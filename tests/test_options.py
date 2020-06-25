import mcddns.options as options


def test_parse():
    args = "test.DNS -a test.Address test.example.com"
    opts = options.parse(args=args.split())

    assert opts.address_providers == ["test.Address"]
    assert opts.dns_provider == "test.DNS"
    assert opts.fqdn == "test.example.com"
