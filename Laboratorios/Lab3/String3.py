from DataStructures import LinkedList

def brokenKey(text):
    ll = LinkedList()
    for i in range(len(text)):
        ll.insert(text[len(text)-i-1])
    print(ll)

    fffirst = ll.first
    lastBefore = None
    auxObj = ll.first
    movingObj = ll.first
    acumn = 0
    while acumn < 20:
        firstObj = ll.first
        if str(movingObj) == '[':
            ll.first = movingObj.next
            ll.last.next = firstObj
            ll.last = movingObj.prev
            movingObj.prev.next= None
            movingObj = ll.first
        elif str(movingObj) == ']':
            '''
            ll.last.next = movingObj
            movingObj.prev.next = fffirst
            ll.last = fffirst.prev
            movingObj = ll.first
            print(ll)
            '''
        elif movingObj.next == None:
            break
        movingObj = movingObj.next
        print(ll)
        acumn += 1

    acum = ""
    for link in ll:
        acum += link
    print(acum)
brokenKey('Thi[s_[ooois_a_[Beiju]_text')
