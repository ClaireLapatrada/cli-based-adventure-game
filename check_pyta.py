if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['hashlib']
    })
    used = False
    while not used:
        inp = input(">> ").strip().lower()

        if len(inp.split()) >= 2:
            do, item = inp.split(' ', 1)
            if do == 'use':
                pass
                while not used:
                    pass
                    if used:
                        pass
                    else:
                        pass
                pass

        elif inp == "use":
            print("Use what?")

        elif inp == 'asd':
            pass

        else:
            print("You are not sure what to do with that.")
