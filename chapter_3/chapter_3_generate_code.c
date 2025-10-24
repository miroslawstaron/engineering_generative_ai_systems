#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <cjson/cJSON.h>

// Structure to hold the memory for the response data
struct MemoryStruct {
    char *memory;
    size_t size;
};

// Callback function to write data received from the server into memory
static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;

    // Reallocate memory to accommodate the new data
    char *ptr = realloc(mem->memory, mem->size + realsize + 1);
    if (ptr == NULL) {
        printf("Not enough memory (realloc returned NULL)\n");
        return 0;
    }

    mem->memory = ptr;
    // Copy the new data into the memory
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0; // Null-terminate the string

    return realsize;
}

// Function to generate code based on the given task
char *generateCode(const char *strTask) {
    CURL *curl;
    CURLcode res;
    struct MemoryStruct chunk;

    chunk.memory = malloc(1); // Initial memory allocation
    chunk.size = 0; // Initial size

    curl_global_init(CURL_GLOBAL_ALL); // Initialize CURL globally
    curl = curl_easy_init(); // Initialize CURL easy session

    if (curl) {
        const char *url = "http://deeperthought.cse.chalmers.se:5050/api/generate";
        const char *model = "llama3.2";
        char data[512];
        // Prepare the JSON data to send in the POST request
        snprintf(data, sizeof(data), "{\"model\":\"%s\",\"prompt\":\"The program to %s is:\",\"stream\":false}", model, strTask);

        struct curl_slist *headers = NULL;
        headers = curl_slist_append(headers, "Content-Type: application/json");

        // Set CURL options for the POST request
        curl_easy_setopt(curl, CURLOPT_URL, url);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data);
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);

        // Perform the request
        res = curl_easy_perform(curl);

        if (res != CURLE_OK) {
            // Print error message if the request failed
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
        } else {
            // Parse the JSON response
            cJSON *json = cJSON_Parse(chunk.memory);
            if (json == NULL) {
                fprintf(stderr, "Error parsing JSON response\n");
            } else {
                // Extract the "response" field from the JSON
                cJSON *response = cJSON_GetObjectItemCaseSensitive(json, "response");
                if (cJSON_IsString(response) && (response->valuestring != NULL)) {
                    // Duplicate the response string
                    char *strProgram = strdup(response->valuestring);
                    cJSON_Delete(json);
                    curl_easy_cleanup(curl);
                    free(chunk.memory);
                    curl_global_cleanup();
                    return strProgram; // Return the generated program
                }
                cJSON_Delete(json);
            }
        }
        curl_easy_cleanup(curl); // Clean up CURL easy session
    }
    free(chunk.memory); // Free the allocated memory
    curl_global_cleanup(); // Clean up CURL globally
    return NULL; // Return NULL if the generation failed
}

int main() {
    const char *task = "Generate a C program to sort an array";
    char *program = generateCode(task); // Generate the program based on the task
    if (program) {
        // Print the generated program
        printf("Generated Program:\n%s\n", program);
        free(program); // Free the allocated memory for the program
    } else {
        printf("Failed to generate program.\n");
    }
    return 0;
}