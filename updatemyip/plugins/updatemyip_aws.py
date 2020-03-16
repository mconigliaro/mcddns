import boto3
import botocore.exceptions as be
import logging as log
import updatemyip.plugin as plugin


@plugin.register_plugin_options("route53")
def options(*args, **kwargs):
    parser = kwargs["parser"]
    parser.add_argument("--aws-route53-hosted-zone-id", default="CHANGE_ME")


@plugin.register_dns_plugin()
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
            curr_name = rrsets[0]["Name"].rstrip(".")
            curr_ttl = rrsets[0]["TTL"]
            curr_type = rrsets[0]["Type"]
            curr_records = rrsets[0]["ResourceRecords"]
            curr_address = " ".join(r["Value"] for r in curr_records)

            log.info(
                f"Current DNS record: {curr_name} {curr_ttl} {curr_type} {curr_address}"
            )

            if curr_type != options.dns_rrtype:
                changes.append({"Action": "DELETE", "ResourceRecordSet": rrsets[0]})
            elif curr_ttl == options.dns_ttl and curr_records == records:
                return plugin.PLUGIN_STATUS_NOOP
        else:
            log.info(f"DNS record not found: {options.fqdn}")

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

        if options.dry_run:
            return plugin.PLUGIN_STATUS_DRY_RUN
        else:
            client.change_resource_record_sets(
                HostedZoneId=options.aws_route53_hosted_zone_id,
                ChangeBatch={"Changes": changes},
            )
            return plugin.PLUGIN_STATUS_SUCCESS

    except be.ClientError as e:
        log.error(f"{e.response['Error']['Code']}: {e.response['Error']['Message']}")
        return plugin.PLUGIN_STATUS_FAILURE
