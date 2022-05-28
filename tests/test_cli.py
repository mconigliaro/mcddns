import mcddns.cli as cli


def test_parse():
    args = "test.DNS -a test.Address test.example.com"
    opts = cli.parse(args=args.split())

    assert opts.address_providers == ["test.Address"]
    assert opts.dns_provider == "test.DNS"
    assert opts.fqdn == "test.example.com"
