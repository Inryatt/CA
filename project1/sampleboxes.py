with open("extras/sboxes/sampleboxes","w+") as f:
    for j in range(16):
        for i in range(1,257):
            bit = (j+ i) %256
            f.write(hex(bit))
            if i==256:
                f.write('\n')
            else:
                f.write(', ')