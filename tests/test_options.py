import updatemyip.options as options


def test_parse():
    args = ["foo.example.com", "-a", "test.Address", "-d", "test.DNS"]
    opts = options.parse(args)

    assert opts.fqdn == args[0]
    assert opts.address_plugin == [args[2]]
    assert opts.dns_plugin == args[4]
