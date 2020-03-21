import updatemyip.options as opt


def test_parse():
    args = "-a test.Address test.DNS test.example.com"
    opts = opt.parse(args.split())

    assert opts.address_providers == ["test.Address"]
    assert opts.dns_provider == "test.DNS"
    assert opts.fqdn == "test.example.com"
