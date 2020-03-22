import boto3
import botocore.client as bc
import botocore.exceptions as be
import logging as log
import updatemyip.exceptions as exc
import updatemyip.provider as pro


class CheckIP(pro.AddressProvider):

    def fetch(self, options):
        return self._fetch_url(options, "https://checkip.amazonaws.com/")


class Route53(pro.DNSProvider):

    def options_pre(self, parser):
        parser.add_argument("hosted_zone_id")

    def check(self, options, address):
        if options.fqdn.endswith("."):
            fqdn = options.fqdn
        else:
            fqdn = f"{options.fqdn}."
        records = [{"Value": address}]

        self.changes = []

        try:
            config = bc.Config(connect_timeout=options.timeout,
                               retries={'max_attempts': 0})
            self.client = boto3.client("route53", config=config)
            rrsets = self.client.list_resource_record_sets(
                HostedZoneId=options.hosted_zone_id,
                StartRecordName=fqdn,
                MaxItems="1",
            )["ResourceRecordSets"]

        except (be.ConnectionError, be.ClientError) as e:
            raise exc.ProviderError(e) from e

        if rrsets and rrsets[0]["Name"] == fqdn:
            cur_name = rrsets[0]["Name"].rstrip(".")
            cur_ttl = rrsets[0]["TTL"]
            cur_type = rrsets[0]["Type"]
            cur_records = rrsets[0]["ResourceRecords"]
            cur_address = " ".join(r["Value"] for r in cur_records)
            cur_record = f"{cur_name} {cur_ttl} {cur_type} {cur_address}"
            log.debug(
                f"Current DNS record: {cur_record}"
            )

            if cur_type != options.rrtype:
                self.changes.append({
                    "Action": "DELETE",
                    "ResourceRecordSet": rrsets[0]
                })
            elif cur_ttl == options.ttl and cur_records == records:
                return False
        else:
            log.debug(f"DNS record not found: {options.fqdn}")

        self.changes.append({
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": fqdn,
                "Type": options.rrtype,
                "TTL": options.ttl,
                "ResourceRecords": records,
            },
        })

        return True

    def update(self, options, address):
        try:
            self.client.change_resource_record_sets(
                HostedZoneId=options.hosted_zone_id,
                ChangeBatch={"Changes": self.changes},
            )

        except (be.ConnectionError, be.ClientError) as e:
            raise exc.ProviderError(e) from e

        return True
