#include <iostream>
#include <vector>
#include <cstdint>

using namespace std;
const int HEADER_PULSE = 9000;
const int HEADER_SPACE = -4500;
const int ONE_PULSE = 560;
const int ONE_SPACE = -1690;
const int ZERO_PULSE = 560;
const int ZERO_SPACE = -560;
const int FOOTER = 560;

vector<int> generateRawIR(uint16_t hexCode) {
    vector<int> rawIR;
    
    // Header
    rawIR.push_back(HEADER_PULSE);
    rawIR.push_back(HEADER_SPACE);
    
    // Convert each bit from MSB to LSB
    for (int i = 8; i >= 0; i--) {
        if (hexCode & (1 << i)) {
            // Bit 1
            rawIR.push_back(ONE_PULSE);
            rawIR.push_back(ONE_SPACE);
        } else {
            // Bit 0
            rawIR.push_back(ZERO_PULSE);
            rawIR.push_back(ZERO_SPACE);
        }
    }
    
    // Footer
    rawIR.push_back(FOOTER);    
    return rawIR;
}

int main() 
{
    int n = 2;
    uint16_t hexCode[n] = {0xF0, 0b11110000};
    for (int i=0; i<n; i++) {
        vector<int> rawIR = generateRawIR(hexCode[i]);
        // Print raw IR signal
        cout<<"[";
        for (size_t j = 0; j < rawIR.size()-1; j++) {
            cout << rawIR[j] << ", ";            
        }
        cout <<rawIR[rawIR.size()-1] <<"]" <<endl;
    }            
     
    return 0;
}
