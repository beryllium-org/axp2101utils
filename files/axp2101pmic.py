rename_process("axp2101pmic")
vr("opts", be.api.xarg())
be.api.setvar("return", "1")
if "i" in vr("opts")["o"]:
    vr("busn", 0)
    if vr("opts")["o"]["i"] is not None:
        try:
            vr("nbus", vr("opts")["o"]["i"])
            if not vr("nbus").startswith("/dev/i2c"):
                raise RuntimeError
            vr("busn", int(vr("opts")["o"]["i"][-1:]))
        except:
            term.write("Could not parse node, using default.")
    vr("i2c", be.devices["i2c"][vr("busn")])
    try:
        from axp2101 import AXP2101
        vr("axp", AXP2101(vr("i2c")))
        del AXP2101
        be.based.run("mknod AXP2101")
        vr("node", be.api.getvar("return"))
        be.api.subscript("/bin/stringproccessing/devid.py")
        be.devices["AXP2101"][vr("dev_id")] = vr("axp")
        dmtex("Registed /dev/AXP2101_0 Power Management device")
        be.api.setvar("return", "0")
    except:
        dmtex("Failed to register AXP2101")
elif "d" in vr("opts")["o"]:
    vr("dev", vr("opts")["o"]["d"])
    if vr("dev") is not None and vr("dev").startswith("/dev/AXP2101_"):
        be.based.run("rmnod " + vr("dev")[5:])
        be.api.setvar("return", "0")
    else:
        term.write("Invalid device node!")
else:
    term.write("Usage:\n    axp2101pmic -i\n    axp2101pmic -d")
