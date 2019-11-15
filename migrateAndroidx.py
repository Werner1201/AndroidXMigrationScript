import fileinput
import os
import re
import sys

gradlewrapperpropspath = "android/gradle/wrapper/gradle-wrapper.properties"
buildgradlepath = "android/build.gradle"
gradleprops = "android/gradle.properties"
androidappbuildgradle = "android/app/build.gradle"


def primeiropasso():
    existe = 0
    for linha in fileinput.FileInput(gradlewrapperpropspath, inplace=True, backup=".bak"):
        if linha == "distributionUrl=https\\://services.gradle.org/distributions/gradle-4.10.2-all.zip\n":
            existe = 1
            sys.stdout.write(linha)           # faz nada
        else:
            sys.stdout.write(linha)

    if existe > 0:
        return True
    else:
        return False


def segundopasso():
    for line in fileinput.FileInput(buildgradlepath, inplace=True, backup=".bak"):
        line = line.replace(
            "classpath 'com.android.tools.build:gradle:3.2.1'", "classpath 'com.android.tools.build:gradle:3.3.0'")
        sys.stdout.write(line)


def terceiropasso():
    with open(gradleprops, "a") as gradlefile:
        gradlefile.write(
            "android.enableJetifier=true\nandroid.useAndroidX=true")
        gradlefile.close()


def quartopasso():
    sdk28 = 0
    for linha in fileinput.FileInput(androidappbuildgradle, inplace=True, backup=".bak"):
        if linha == "    compileSdkVersion 28\n":
            sdk28 += 1
            sys.stdout.write(linha)

        elif linha == "        targetSdkVersion 28\n":
            sdk28 += 1
            sys.stdout.write(linha)

        elif linha == "        testInstrumentationRunner \"android.support.test.runner.AndroidJUnitRunner\"\n":
            sdk28 += 1
            linha = linha.replace(
                "        testInstrumentationRunner \"android.support.test.runner.AndroidJUnitRunner\"", "        testInstrumentationRunner \"androidx.test.runner.AndroidJUnitRunner\"" + "\n        multiDexEnabled true")
            sys.stdout.write(linha)

        elif linha == "    androidTestImplementation 'com.android.support.test:runner:1.0.2'\n":
            sdk28 += 1
            linha = linha.replace("androidTestImplementation 'com.android.support.test:runner:1.0.2'",
                                  "androidTestImplementation 'androidx.test:runner:1.1.1'")
            sys.stdout.write(linha)

        elif linha == "    androidTestImplementation 'com.android.support.test.espresso:espresso-core:3.0.2'\n":
            sdk28 += 1
            linha = linha.replace(
                "androidTestImplementation 'com.android.support.test.espresso:espresso-core:3.0.2'", "androidTestImplementation 'androidx.test.espresso:espresso-core:3.1.1'")
            sys.stdout.write(linha)
        else:
            sys.stdout.write(linha)

    if sdk28 == 5:
        return True
    else:
        return False


def main():
    primeiropasso()
    segundopasso()
    terceiropasso()
    quartopasso()


main()
