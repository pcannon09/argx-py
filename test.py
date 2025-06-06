import sys
import build.argx_py as argx

def main():
    doc_str = ""

    mainArgx = argx.Argx("main-args", sys.argv)

    # Setup mainArgx
    helpOption = argx.ARGXOptions()
    versionOption = argx.ARGXOptions()
    styleOption = argx.ARGXOptions()

    helpOption.id = "help"
    helpOption.param = "--help"
    helpOption.sparam = "-h"
    helpOption.info = "Show this help"
    helpOption.hasSubParams = True

    versionOption.id = "version"
    versionOption.param = "--version"
    versionOption.sparam = "-v"
    versionOption.info = "Show version message"
    versionOption.hasSubParams = False

    styleOption.id = "style"
    styleOption.param = "--style"
    styleOption.sparam = "-s"
    styleOption.info = "Set the style of the documentation (simple OR professional)"
    styleOption.hasSubParams = True

    versionSubOption = argx.ARGXOptions()
    messageSubOption = argx.ARGXOptions()
    styleSubOptionSimple = argx.ARGXOptions()
    styleSubOptionPro = argx.ARGXOptions()

    versionSubOption.id = "version"
    versionSubOption.param = "version"
    versionSubOption.sparam = "v"
    versionSubOption.info = "Show version help"
    versionSubOption.hasSubParams = False

    messageSubOption.id = "message"
    messageSubOption.param = "message"
    messageSubOption.sparam = "m"
    messageSubOption.info = "Show a specific message"
    messageSubOption.hasSubParams = False

    styleSubOptionSimple.id = "simple"
    styleSubOptionSimple.param = "simple"
    styleSubOptionSimple.info = "Set simple documentation"
    styleSubOptionSimple.hasSubParams = False

    styleSubOptionPro.id = "professional"
    styleSubOptionPro.param = "professional"
    styleSubOptionPro.sparam = "pro"
    styleSubOptionPro.info = "Set professional documentation"
    styleSubOptionPro.hasSubParams = False

    styleOption.subParams.push_back(styleSubOptionSimple)
    styleOption.subParams.push_back(styleSubOptionPro)

    helpOption.subParams.push_back(versionSubOption)
    helpOption.subParams.push_back(messageSubOption)

    versionOption.subParams.push_back(versionSubOption)

    mainArgx.add(helpOption)
    mainArgx.add(versionOption)
    mainArgx.add(styleOption)

    msg = "Simple documentation on how to use the ARGX test"

    if mainArgx.getParam("style").exists:
        if mainArgx.getArgc() > 2:
            if mainArgx.getMainArgs()[2] == "simple":
                doc_str = mainArgx.createDocs(argx.ARGXStyle_Simple, "-- Docs ----", msg)
            else:
                doc_str = mainArgx.createDocs(argx.ARGXStyle_Professional, "-- Docs ----", msg)
        else:
            print("Set one of those two values:")
            print("* simple")
            print("* professional")
            print("NOTE: You can code your own documentation by overriding the Argx::createDocs() function")
            return 1
    else:
        doc_str = mainArgx.createDocs(argx.ARGXStyle_Professional, "-- Docs ----", msg)

    if mainArgx.getArgc() <= 1:
        print(doc_str)
        return 0

    if mainArgx.getParam("help").exists:
        helpParam = mainArgx.getParam("help")

        if mainArgx.getSubParam(helpParam, "version"):
            print("For more information, call the following parameter: `--version`")
        elif mainArgx.getSubParam(helpParam, "message"):
            if mainArgx.getArgc() > 3:
                print(mainArgx.getMainArgs()[3])
            else:
                print("Enter a message in the third parameter as a string")

        print(doc_str)

    if mainArgx.getParam("version").exists:
        print("ARGX Version information:")
        print(f"Version: {argx.ARGX_VERSION_MAJOR}.{argx.ARGX_VERSION_MINOR}.{argx.ARGX_VERSION_PATCH} {argx.ARGX_VERSION_STATE}")
        print(f"Version Standard: {argx.ARGX_VERSION_STD}")
        print(f"Development Type: {'DEV' if argx.ARGX_DEV else 'PRODUCTION'}")

    if not mainArgx.compareArgs(mainArgx.getOptions(), mainArgx.getMainArgs()):
        arg = mainArgx.getMainArgs()[1] if mainArgx.getArgc() > 1 else "<UNKNOWN>"
        print(f"Argx: Unknown option `{arg}`")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

