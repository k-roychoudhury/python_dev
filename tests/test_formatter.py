x = """select art, decode(PO,' ','SP',NULL,'NO','YES') PA,  decode(ACCOUNT_CODE,' ','SP',NULL,'NO','YES') ACNT,  decode(ttyp_4210_rec,0,'NO','YES') TTYP4210,  decode(ttyp_4212_rec,0,'NO','YES') TTYP4212,  decode(ttyp_4241_rec,0,'NO','YES') TTYP4242,  decode(ass1,'A','YES','K','YES','Ö','YES','O','YES','NO') TTYP5031,  decode( (select count(*) from new_art_descr where art=a.art and ADSC_UNICODE <> ' '), 0 , 'NO','YES') DESCR,  decode( (select count(*) from v_dwp_item_rcv where art=a.art), 0 , 'NO','YES') DWP_RCV,  decode( (select count(*) from v_dwp_item_rcv_cp where art=a.art), 0 , 'NO','YES') DWP_RCV_CP,  decode( (select count(*) from v_dwp_item where art=a.art), 0 , 'NO','YES') DWP,  decode( (select count(*) from v_dwp_item_cp where art=a.art), 0 , 'NO','YES') DWP_CP,ITEM_TYPE  from NEW_ART a where art in ('30472692', '00472679', '80472350', '50472361', '30472381', '50472375', '60472638', '90472632', '50438273', '60438338', '60438343', '60443759', '00438360', '00455378', '60443764', '50438353', '00455383', '50443769', '90455388', '30438368', '30484845', '30472625', '10472301', '30472296', '40472272', '50472196', '40472187', '30479226');"""\

import re


def fact(n: int) -> int:
    return 1 if n <=0 else n*fact(n-1)

def splitter(string: str, result: list, buffer_length=1024) -> None:
    #print("string: {},\nstring length: {}".format(string, len(string)))
    if len(string) < buffer_length:
        result.append(string)
        return
    else:
        i = 0
        last_break_point = 0
        while i < buffer_length:   
            if string[i] == ' ':
                last_break_point = i
                i += 1
                continue
            elif string[i] == "'" or string[i] == "\"":
                # do shit
                last_break_point = i
                j = i+1
                while j < buffer_length:
                    if string[j] == "'" or string[j] == "\"":
                        i = j+1
                        last_break_point = i
                        break
                    else:
                        j += 1
                if j >= buffer_length:
                    #print("char broken at: {}, index: {}".format(string[last_break_point], last_break_point))
                    result.append(string[0: last_break_point])
                    splitter(string[last_break_point: ], result, buffer_length)
                    return
            else:
                i += 1
                continue
        #print("char broken at: {}, index: {}".format(string[last_break_point], last_break_point))
        result.append(string[0: last_break_point])
        splitter(string[last_break_point: ], result, buffer_length)
        return


if __name__ == "__main__":
    #print(fact(5))
    print(x)
    #y = re.split("[ '\"]", x)
    #print(y)
    #print(" ".join(y))
    y = list()
    splitter(x, y)
    print(y)


    # print(x)
    # a = [m.start() for m in re.finditer("['\"]", x)]
    # #print(a, len(a))
    # b = [(a[i], a[i+1]) for i in range(0, len(a)-1, 2)]
    # b.insert(0, (0, b[0][0]-1))
    # b.append((b[-1][1]+1, len(x)))
    # print(b, len(b))

    # result = list()
    # i = 0
    # threshold = 1024
    # left, right = b[i]
    # while i < len(b)-1:
    #     if b[i+1][1] <= threshold:
    #         right = b[i+1][1]
    #         i += 1
    #     else:
    #         right = b[i+1][0]-1
    #         result.append((left, right))
    #         left = b[i+1][0]
    #         threshold = left + 1024
    # result.append((left, right))

    # print(result)