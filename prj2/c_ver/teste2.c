#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <nettle/rsa.h>
#include <nettle/bignum.h>

int main(int argc, char *argv[])
{
    if (argc != 3) {
        printf("Usage: %s <public_key.pem> <private_key.pem>\n", argv[0]);
        return 1;
    }

    char *pub_file = argv[1];
    char *priv_file = argv[2];

    struct rsa_public_key pub;
    struct rsa_private_key priv;
    rsa_public_key_init(&pub);
    rsa_private_key_init(&priv);

   

    FILE *fp;

    /* Load public key */
    fp = fopen(pub_file, "r");
    if (fp == NULL) {
        printf("Error opening file %s for reading public key data\n", pub_file);
        return 1;
    }
    if (pem_read_rsa_public_key(fp, &ctx, &pub) != 1) {
        printf("Error reading public key data from file %s\n", pub_file);
        return 1;
    }
    fclose(fp);

    /* Load private key */
    fp = fopen(priv_file, "r");
    if (fp == NULL) {
        printf("Error opening file %s for reading private key data\n", priv_file);
        return 1;
    }
    if (pem_read_rsa_private_key(fp, &ctx, &priv) != 1) {
        printf("Error reading private key data from file %s\n", priv_file);
        return 1;
    }
    fclose(fp);

    printf("Key pair successfully loaded from files\n");
    return 0;
}
