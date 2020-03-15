import boto3
import botocore.exceptions as be
import logging as log
import updatemyip.plugin as plugin


# FIXME: How to deal with required plugin options?
@plugin.register_options("route53")
def options(*args, **kwargs):
    parser = kwargs["parser"]
    parser.add_argument("--aws-route53-hosted-zone-id", default="CHANGE_ME")


@plugin.register_plugin(plugin.PLUGIN_TYPE_DNS)
def route53(*args, **kwargs):
    options = kwargs["options"]
    fqdn = options.fqdn if options.fqdn.endswith(".") else f"{options.fqdn}."
    records = [{"Value": kwargs["address"]}]

    try:
        client = boto3.client("route53")

        rrsets = client.list_resource_record_sets(
            HostedZoneId=options.aws_route53_hosted_zone_id,
            StartRecordName=fqdn,
            MaxItems="1",
        )["ResourceRecordSets"]

        changes = []
        if rrsets and rrsets[0]["Name"] == fqdn:
            if rrsets[0]["Type"] != options.dns_rrtype:
                changes.append({"Action": "DELETE", "ResourceRecordSet": rrsets[0]})
            elif rrsets[0]["ResourceRecords"] == records:
                return plugin.PLUGIN_STATUS_NOOP

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

        client.change_resource_record_sets(
            HostedZoneId=options.aws_route53_hosted_zone_id,
            ChangeBatch={"Changes": changes},
        )
        return plugin.PLUGIN_STATUS_SUCCESS

    except be.ClientError as e:
        log.error(f"{e.response['Error']['Code']}: {e.response['Error']['Message']}")
        return plugin.PLUGIN_STATUS_FAILURE
