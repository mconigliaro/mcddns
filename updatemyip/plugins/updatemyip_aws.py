import boto3
import botocore.exceptions as be
import logging as log
import updatemyip.plugin as pi


class Route53(pi.DNSPlugin):

    def options(self, parser):
        parser.add_argument("--aws-route53-hosted-zone-id",
                            default="CHANGE_ME")

    # FIXME: Implement
    def check(self, options, address):
        return True

    def update(self, options, address):
        if options.fqdn.endswith("."):
            fqdn = options.fqdn
        else:
            fqdn = f"{options.fqdn}."
        records = [{"Value": address}]

        try:
            client = boto3.client("route53")

            rrsets = client.list_resource_record_sets(
                HostedZoneId=options.aws_route53_hosted_zone_id,
                StartRecordName=fqdn,
                MaxItems="1",
            )["ResourceRecordSets"]

            changes = []
            if rrsets and rrsets[0]["Name"] == fqdn:
                cur_name = rrsets[0]["Name"].rstrip(".")
                cur_ttl = rrsets[0]["TTL"]
                cur_type = rrsets[0]["Type"]
                cur_records = rrsets[0]["ResourceRecords"]
                cur_address = " ".join(r["Value"] for r in cur_records)
                cur_record = f"{cur_name} {cur_ttl} {cur_type} {cur_address}"
                log.info(
                    f"Current DNS record: {cur_record}"
                )

                if cur_type != options.dns_rrtype:
                    changes.append({
                        "Action": "DELETE",
                        "ResourceRecordSet": rrsets[0]
                    })
                elif cur_ttl == options.dns_ttl and cur_records == records:
                    return pi.PLUGIN_STATUS_NOOP
            else:
                log.info(f"DNS record not found: {options.fqdn}")

            changes.append({
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": fqdn,
                    "Type": options.dns_rrtype,
                    "TTL": options.dns_ttl,
                    "ResourceRecords": records,
                },
            })

            if options.dry_run:
                return pi.PLUGIN_STATUS_DRY_RUN
            else:
                client.change_resource_record_sets(
                    HostedZoneId=options.aws_route53_hosted_zone_id,
                    ChangeBatch={"Changes": changes},
                )
                return pi.PLUGIN_STATUS_SUCCESS

        except be.ClientError as e:
            code = e.response['Error']['Code']
            msg = e.response['Error']['Message']
            log.warning(f"{code}: {msg}")
            return pi.PLUGIN_STATUS_FAILURE
