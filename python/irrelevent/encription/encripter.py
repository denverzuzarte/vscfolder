import key_generator
n=key_generator.key1;
message="jhafajlkshfuiaehigdc";
def encriptor(key,message):
    tot=0;
    new_enc='';
    for m in message:
        tot=0;
        for char in key:
            tot=tot+ord(char);
        new_enc=new_enc+chr(tot%128);
    return new_enc;
ask=encriptor(n,message);