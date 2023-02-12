package ca.p2.ec;

import org.bouncycastle.asn1.pkcs.PrivateKeyInfo;
import org.bouncycastle.jce.provider.BouncyCastleProvider;
import org.bouncycastle.openssl.PEMException;
import org.bouncycastle.openssl.PEMKeyPair;
import org.bouncycastle.openssl.PEMParser;
import org.bouncycastle.openssl.jcajce.JcaPEMKeyConverter;
import org.bouncycastle.pkcs.PKCS8EncryptedPrivateKeyInfo;
import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemReader;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.security.*;
import java.security.spec.ECPrivateKeySpec;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.ArrayList;
import java.util.Arrays;


public class EC_Main {


    public static PublicKey ecGetPubkey(String curve_name, String key_size) throws NoSuchAlgorithmException, IOException {
        Security.addProvider(new BouncyCastleProvider());
        KeyFactory factory = KeyFactory.getInstance("EC");
        //System.out.println("Working Directory = " + System.getProperty("user.dir"));
        File pubkeyfile = new File("../../keys/" + curve_name + "_" + key_size + "_public_key.pem");

        try (FileReader keyReader = new FileReader(pubkeyfile);
             PemReader pemReader = new PemReader(keyReader)) {

            PemObject pemObject = pemReader.readPemObject();
            byte[] content = pemObject.getContent();
            X509EncodedKeySpec pubKeySpec = new X509EncodedKeySpec(content);
            return factory.generatePublic(pubKeySpec);
        } catch (IOException | InvalidKeySpecException e) {
            throw new IOException(e);
        }
    }

    public static byte[] GenerateSignature(String plaintext, KeyPair keys) throws SignatureException, UnsupportedEncodingException, InvalidKeyException, NoSuchAlgorithmException, NoSuchProviderException {

        Security.addProvider(new BouncyCastleProvider());
        Signature ecdsaSign = Signature.getInstance("SHA256withECDSA", "BC");
        ecdsaSign.initSign(keys.getPrivate());
        ecdsaSign.update(plaintext.getBytes(StandardCharsets.UTF_8));
        return ecdsaSign.sign();
    }

    public static boolean ValidateSignature(String plaintext, KeyPair pair, byte[] signature) throws SignatureException, InvalidKeyException, UnsupportedEncodingException, NoSuchAlgorithmException, NoSuchProviderException {
        Security.addProvider(new BouncyCastleProvider());
        Signature ecdsaVerify = Signature.getInstance("SHA256withECDSA", "BC");
        ecdsaVerify.initVerify(pair.getPublic());
        ecdsaVerify.update(plaintext.getBytes(StandardCharsets.UTF_8));
        return ecdsaVerify.verify(signature);
    }

    public static void main(String[] args) throws IOException {
        String[] curves = new String[]{"nistp", "nistk", "nistb"};
        String[] key_sizes = new String[]{"small", "medium", "large"};
        int m = 100;
        int n = 1000;
        for (String curve : curves) {
            for (String key_size : key_sizes) {
                try {
                    PublicKey pubkey = ecGetPubkey(curve, key_size);
                    PrivateKey privkey = ecGetPrivkey(curve, key_size);
                    KeyPair keys = new KeyPair(pubkey, privkey);
                    String plaintext = "this is a message";
                    ArrayList<Long> speeds = new ArrayList<>();
                    for (int i=0;i<n;i++){
                        long startTime = System.nanoTime();
                        for(int j=0;j<m;j++){
                            byte[] signature = GenerateSignature(plaintext, keys);
                             if (!ValidateSignature(plaintext, keys, signature)) {
                                 System.exit(1);
                            }
                        }

                        long endTime = System.nanoTime();
                        speeds.add((endTime - startTime));
                    }
                    //minimum value in speeds
                    long min = speeds.stream().mapToLong(v -> v).min().orElseThrow(RuntimeException::new);
                    min=min/m;

                    System.out.println(curve + "_" + key_size + ": " +min +"ns");
                } catch (NoSuchAlgorithmException | NoSuchProviderException | InvalidKeyException | SignatureException |
                         UnsupportedEncodingException | InvalidKeySpecException e) {
                    e.printStackTrace();
                }
            }
        }

    }

    private static PrivateKey ecGetPrivkey(String curve_name, String key_size) throws IOException, NoSuchAlgorithmException, InvalidKeySpecException {


        File privKeyFile = new File("../../keys/" + curve_name + "_" + key_size + "_private_key.pem");
        Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());

        Object parsed = new org.bouncycastle.openssl.PEMParser(new FileReader(privKeyFile)).readObject();
        KeyPair pair = new org.bouncycastle.openssl.jcajce.JcaPEMKeyConverter().getKeyPair((org.bouncycastle.openssl.PEMKeyPair)parsed);
        return pair.getPrivate();

    }
}
