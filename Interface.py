Ask=input('Choose interface mode:\n1.WordleBot\n2.Game with support\nElse to stop\n')
while Ask.isdigit():
    if Ask=='1':
        import INTERFACE.WordleBot as WordleBot
    if Ask=='2':
        import INTERFACE.Gamewithsupport as Gamewithsupport
    Ask=input('Choose interface mode:\n1.WordleBot\n2.Game with support\nElse to stop\n')
