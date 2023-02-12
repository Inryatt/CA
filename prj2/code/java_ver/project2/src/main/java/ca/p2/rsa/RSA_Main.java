package ca.p2.rsa;

import org.bouncycastle.util.io.pem.PemObject;
import org.bouncycastle.util.io.pem.PemReader;
import org.bouncycastle.jce.provider.BouncyCastleProvider;

import java.io.File;
import java.io.FileReader;
import java.security.*;
import java.security.spec.X509EncodedKeySpec;
import java.util.ArrayList;
import java.util.Arrays;

import static java.lang.System.exit;


public class RSA_Main {

    // https://github.com/rodbate/bouncycastle-examples/blob/master/src/main/java/bcfipsin100/base/Rsa.java
    // for the code snippets for signing
    // and https://www.baeldung.com/java-read-pem-file-keys for loading keys

    public static byte[] generatePkcs1Signature(PrivateKey rsaPrivate, byte[] input)
            throws GeneralSecurityException {
        Security.addProvider(new BouncyCastleProvider());
        Signature signature = Signature.getInstance("SHA256withRSA", "BC");
        signature.initSign(rsaPrivate);
        signature.update(input);
        return signature.sign();
    }

    public static boolean verifyPkcs1Signature(PublicKey rsaPublic, byte[] encSignature, byte[] input)
            throws GeneralSecurityException {
        Security.addProvider(new BouncyCastleProvider());
        Signature signature = Signature.getInstance("SHA256withRSA", "BC");
        signature.initVerify(rsaPublic);
        signature.update(input);
        return signature.verify(encSignature);
    }

    public static byte[] generatePssSignature(PrivateKey rsaPrivate, byte[] input)
            throws GeneralSecurityException {
        Signature signature = Signature.getInstance("SHA256withRSA", "BC");
        signature.initSign(rsaPrivate);
        signature.update(input);
        return signature.sign();
    }

    public static boolean verifyPssSignature(PublicKey rsaPublic, byte[] encSignature, byte[] input)
            throws GeneralSecurityException {
        Signature signature = Signature.getInstance("SHA256withRSA", "BC");
        signature.initVerify(rsaPublic);
        signature.update(input);
        return signature.verify(encSignature);
    }

    public static PublicKey rsaGetPubkey(int key_size) throws Exception {
        KeyFactory factory = KeyFactory.getInstance("RSA");
        //System.out.println("Working Directory = " + System.getProperty("user.dir"));
        File pubkeyfile = new File("../../keys/" + key_size + "_public_key.pem");

        try (FileReader keyReader = new FileReader(pubkeyfile);
             PemReader pemReader = new PemReader(keyReader)) {

            PemObject pemObject = pemReader.readPemObject();
            byte[] content = pemObject.getContent();
            X509EncodedKeySpec pubKeySpec = new X509EncodedKeySpec(content);
            return factory.generatePublic(pubKeySpec);
        }
    }

    public static PrivateKey rsaGetPrivkey(int key_size) throws Exception {

        KeyFactory factory = KeyFactory.getInstance("RSA");
        File privkeyFile = new File("../../keys/" + key_size + "_private_key.pem");
        try (FileReader keyReader = new FileReader(privkeyFile);
             PemReader pemReader = new PemReader(keyReader)) {

            PemObject pemObject = pemReader.readPemObject();
            byte[] content = pemObject.getContent();

            java.security.spec.KeySpec spec = new java.security.spec.PKCS8EncodedKeySpec(content);
            return java.security.KeyFactory.getInstance("RSA", new BouncyCastleProvider()).generatePrivate(spec);
        }
    }

    public static void main(String[] args) throws NoSuchAlgorithmException {
        // import a key pair
        long start = 0, end = 0;
        int[] key_sizes = new int[]{1024, 2048, 4096};
        for (int key_size : key_sizes) {
            PublicKey pubkey = null;
            try {
                pubkey = rsaGetPubkey(key_size);
            } catch (Exception e) {
                e.printStackTrace();
                System.out.println("ERROR LOADING PUBKEY " + key_size);
                exit(1);
            }
            PrivateKey privkey = null;
            try {
                privkey = rsaGetPrivkey(key_size);
            } catch (Exception e) {
                e.printStackTrace();

                System.out.println("ERROR LOADING PRIVKEY " + key_size);
                exit(1);
            }

            // create a message
            String message = "this is a message";
            byte[] data = message.getBytes();
            int m = 100;
            int n = 1000;
            ArrayList<Long> speeds = new ArrayList<>();

            // PKCS1
            for (int i = 0; i < n; i++) {
                long startTime = System.nanoTime();
                for (int j = 0; j < m; j++) {
                    byte[] signature;
                    try {
                        signature = generatePkcs1Signature(privkey, data);
                        if (!verifyPkcs1Signature(pubkey, signature, data)) {
                            System.err.println("Signature doesnt match");
                            exit(1);
                        }


                    } catch (GeneralSecurityException e) {
                        System.err.println("ERROR in PKCS");
                        exit(1);
                    }
                }

                long endTime = System.nanoTime();
                speeds.add((endTime - startTime));
            }
            long min = speeds.stream().mapToLong(v -> v).min().orElseThrow(RuntimeException::new);
            min=min/m;
            System.out.println("Key size: " + key_size + " PKCS1: " + min + " ns");
            speeds = new ArrayList<>();

            // PSS
            for (int i = 0; i < n; i++) {
                long startTime = System.nanoTime();
                for (int j = 0; j < m; j++) {
                    byte[] signature = new byte[0];


                    try {
                        signature = generatePssSignature(privkey, data);
                    } catch (GeneralSecurityException e) {
                        System.err.println("ERROR GENERATING PSS");
                        exit(1);
                    }

                    try {
                        if (!verifyPssSignature(pubkey, signature, data)) {
                            System.err.println("ERROR VERIFYING PSS");
                            exit(1);
                        }
                    } catch (GeneralSecurityException e) {
                        System.err.println("ERROR VERIFYING PSS");
                        exit(1);
                    }
                }
                end = System.nanoTime();
                speeds.add((end - startTime));

            }
            min = speeds.stream().mapToLong(v -> v).min().orElseThrow(RuntimeException::new);
            min=min/m;
            System.out.println("Key size: " + key_size + " PSS: " + min + " ns");


        }


    }
}