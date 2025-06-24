import key_generator
import encripter
n=key_generator.key2;
def decripter(key,message):
    tot=0;
    new_enc='';
    for m in message:
        tot=0;
        for char in key:
            tot=tot-ord(char)+128;
            print(chr(tot%128))
        new_enc=new_enc+chr(tot%128);
    return new_enc;
mystring=decripter(key_generator.key2,encripter.ask);