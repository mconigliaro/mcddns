import boto3
import botocore.client
import logging
import mcddns.provider as provider


class CheckIP(provider.AddressProvider):

    @classmethod
    def fetch(cls, options):
        return cls.fetch_url(
            "https://checkip.amazonaws.com/",
            timeout=options.timeout
        )


class Route53(provider.DNSProvider):

    @classmethod
    def options_pre(cls, parser):
        parser.add_argument(
            "hosted_zone_id",
            help="aws route53 hosted zone id"
        )
        parser.add_argument(
            "--boto-log",
            action="store_true",
            help="show log messages from boto"
        )

    @classmethod
    def options_post(cls, parser, options):
        logging.getLogger("botocore").propagate = options.boto_log

    @classmethod
    def check(cls, options, address):
        if options.fqdn.endswith("."):
            fqdn = options.fqdn
        else:
            fqdn = f"{options.fqdn}."
        records = [{"Value": address}]

        cls.changes = []

        config = botocore.client.Config(connect_timeout=options.timeout,
                                        retries={'max_attempts': 0})
        cls.client = boto3.client("route53", config=config)

        rrsets = cls.client.list_resource_record_sets(
            HostedZoneId=options.hosted_zone_id,
            StartRecordName=fqdn,
            MaxItems="1",
        )["ResourceRecordSets"]

        if rrsets and rrsets[0]["Name"] == fqdn:
            cur_name = rrsets[0]["Name"].rstrip(".")
            cur_ttl = rrsets[0]["TTL"]
            cur_type = rrsets[0]["Type"]
            cur_records = rrsets[0]["ResourceRecords"]
            cur_address = " ".join(r["Value"] for r in cur_records)
            cur_record = f"{cur_name} {cur_ttl} {cur_type} {cur_address}"
            cls.log.debug("Current DNS record: %s", cur_record)

            if cur_type != options.rrtype:
                cls.changes.append({
                    "Action": "DELETE",
                    "ResourceRecordSet": rrsets[0]
                })
            elif cur_ttl == options.ttl and cur_records == records:
                return False
        else:
            cls.log.debug("DNS record not found: %s", options.fqdn)

        cls.changes.append({
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": fqdn,
                "Type": options.rrtype,
                "TTL": options.ttl,
                "ResourceRecords": records,
            }
        })

        return True

    @classmethod
    def update(cls, options, address):
        cls.client.change_resource_record_sets(
            HostedZoneId=options.hosted_zone_id,
            ChangeBatch={"Changes": cls.changes},
        )

        return True
