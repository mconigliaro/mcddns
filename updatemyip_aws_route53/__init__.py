import updatemyip.options as options


options.parser.add_argument("--aws-route53-rrtype", default="A")
options.parser.add_argument("--aws-route53-ttl", type=int, default=300)


def update_dns(**kwargs):
    pass
