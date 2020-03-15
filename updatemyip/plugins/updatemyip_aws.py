import boto3
import botocore.exceptions as be
import logging as log
import updatemyip.options as options
import updatemyip.plugin as plugin


# FIXME: How to deal with required plugin options?
options.parser.add_argument("--aws-route53-hosted-zone-id")


@plugin.register_plugin(plugin.PLUGIN_TYPE_DNS)
def route53(**kwargs):
    options = kwargs["options"]
    fqdn = f"{options.fqdn}."
    records = [{"Value": kwargs["address"]}]

    try:
        client = boto3.client("route53")

        # FIXME: IndexError when no records returned
        record_set = client.list_resource_record_sets(
            HostedZoneId=options.aws_route53_hosted_zone_id,
            StartRecordName=fqdn,
            MaxItems="1",
        )["ResourceRecordSets"][0]

        changes = []
        if record_set["Name"] == fqdn and record_set["Type"] != options.dns_rrtype:
            changes.append({"Action": "DELETE", "ResourceRecordSet": record_set})

        if (
            record_set["Name"] == fqdn and record_set["ResourceRecords"] != records
        ) or record_set["Name"] != fqdn:
            changes.append(
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": fqdn,
                        "Type": options.dns_rrtype,
                        "TTL": options.dns_ttl,
                        "ResourceRecords": records,
                    },
                }
            )

        if changes:
            client.change_resource_record_sets(
                HostedZoneId=options.aws_route53_hosted_zone_id,
                ChangeBatch={"Changes": changes},
            )
            return plugin.PLUGIN_STATUS_SUCCESS
        else:
            return plugin.PLUGIN_STATUS_NOOP

    except be.ClientError as e:
        log.error(f"{e.response['Error']['Code']}: {e.response['Error']['Message']}")
        return plugin.PLUGIN_STATUS_FAILURE
