#include <cryptopp/pem.h>

int load_keys(){

    CryptoPP::RSA::PrivateKey pk;
CryptoPP::FileSource file("<rsa-key-file.pem>", true);

CryptoPP::PEM_Load(file, pk);

CryptoPP::AutoSeededRandomPool prng;
bool = pk.Validate(prng, 3);
}