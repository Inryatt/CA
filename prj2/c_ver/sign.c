#include <nettle/rsa.h>


struct rsa_public_key pub;
struct rsa_private_key priv;


int load_key(char *pub_file, char *priv_file, struct rsa_public_key *pub, struct rsa_private_key *priv)
{

    FILE *fp;
    fp = fopen(pub_file, "r");

    if (fp == NULL)
    {
        printf("Error opening file %s for reading public key data \r \n", pub_file);
        return 1;
    }

    if (rsa_public_key_from_file(pub, fp) != 1)
    {
        printf("Error reading public key data from file %s \r \n", pub_file);
        return 1;
    }

    fclose(fp);
    fp = fopen(priv_file, "r");

    if (fp == NULL)
    {
        printf("Error opening file %s for reading private key data \r \n", priv_file);
        return 1;
    }

    if (rsa_private_key_from_file(priv, fp) != 1)
    {
        printf("Error reading private key data from file %s \r \n", priv_file);
        return 1;
    }

    fclose(fp);
    return 0;
}


int main()
{
    void rsa_public_key_init(struct rsa_public_key * pub);
    void rsa_private_key_init(struct rsa_private_key * priv);

    if (load_key("pub.key", "priv.key", &pub, &priv) != 0){
        printf("Error loading key pair from files \r \n");
        return 1;
    }

    printf("Error loading key pair from files \r \n");
    return 1;
}
