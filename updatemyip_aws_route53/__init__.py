import boto3
import botocore.exceptions as be
import logging as log
import updatemyip.options as options
import updatemyip.plugin as plugin


options.parser.add_argument("--aws-route53-hosted-zone-id")


def update_dns(options, addr):
    fqdn = f"{options['fqdn']}."
    rrs = [{"Value": f"{addr}"}]

    try:
        client = boto3.client("route53")
        rrsets = client.list_resource_record_sets(
            HostedZoneId=options["aws_route53_hosted_zone_id"],
            StartRecordName=fqdn,
            MaxItems="1",
        )["ResourceRecordSets"][0]

        changes = []
        if rrsets["Name"] == fqdn and rrsets["Type"] != options["dns_rrtype"]:
            changes.append({"Action": "DELETE", "ResourceRecordSet": rrsets})

        if (rrsets["Name"] == fqdn and rrsets["ResourceRecords"] != rrs) or rrsets[
            "Name"
        ] != fqdn:
            changes.append(
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": fqdn,
                        "Type": options["dns_rrtype"],
                        "TTL": options["dns_ttl"],
                        "ResourceRecords": rrs,
                    },
                }
            )

        if changes:
            client.change_resource_record_sets(
                HostedZoneId=options["aws_route53_hosted_zone_id"],
                ChangeBatch={"Changes": changes},
            )
            return plugin.PLUGIN_SUCCESS
        else:
            return plugin.PLUGIN_NOOP

    except be.ClientError as e:
        error = e.response["Error"]
        log.error(f"{error['Code']}: {error['Message']}")
        return plugin.PLUGIN_FAILURE
