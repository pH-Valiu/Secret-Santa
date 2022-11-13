#include <QCoreApplication>
#include "qaesencryption.h"

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);


    QTextStream out(stdout);
    QTextStream in(stdin);
    QString inString;
    bool checkMark = true;

    out << "How many little santas will be joining the party?\n";
    out.flush();
    in.readLineInto(&inString);
    int santasCount = inString.toInt(&checkMark);
    QByteArray table[santasCount][2];

    //Filling the table with the names
    for(int i=0; i<santasCount; i++){
        out << "Please enter name of santa "<<(i+1)<<": ";
        out.flush();
        in.readLineInto(&inString);
        table[i][0] = inString.toUtf8();
    }

    //Randomizing the position of the names in the array
    QByteArray temp;
    for(int i=0; i<santasCount; i++){
        int rnd = std::rand() % santasCount;
        temp = table[i][0];
        table[i][0] = table[rnd][0];
        table[rnd][0] = temp;
    }

    //Encrypting the partner for each with given key in AES_128 in ECB mode with PKCS7 padding and output in base64
    QAESEncryption crypter(QAESEncryption::AES_128, QAESEncryption::ECB, QAESEncryption::PKCS7);
    out << "Please enter the key for this secret-santa event (16 Bytes of size): ";
    out.flush();
    in.readLineInto(&inString);

    QByteArray outCipher;
    QByteArray inCipher;
    for(int i=0; i<santasCount; i++){
        inCipher = table[(i+1) % santasCount][0];
        crypter.encode(inCipher, inString.toUtf8(), outCipher);
        table[i][1] = outCipher.toBase64();
        out << "Santa "<<table[i][0]<< " has been assigned to gift to: "<<table[i][1]<<"\n";
        out.flush();
    }


    return a.exec();
}
