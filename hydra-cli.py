import sys
import businesslogic, constants

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Invalid Usage")
        exit(1000)

    if sys.argv[1] == 'unverify':
        if len(sys.argv) < 3:
            print("Invalid Usage")
            exit(1000)

        print('Marking user "' + sys.argv[2] + '" as Unverified')
        print(businesslogic.unverify_user(sys.argv[2]))
        exit(0)

    if sys.argv[1] == 'login':
        print(businesslogic.login(sys.argv[2], sys.argv[3], sys.argv[4]))
        exit(0)

    if sys.argv[1] == 'showencrypt':
        print(constants.USE_ENCRYPTION)
        exit(0)

    if sys.argv[1] == 'refund':
        print(businesslogic.issue_refund(sys.argv[2], False))