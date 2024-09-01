const fs = require('fs')
const dfd = require('danfojs')
const OpenAI = require('openai')
const _ = require('lodash')

const secrectKey = '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'
const openai = new OpenAI({ apiKey: secrectKey })

//**function to map back the answer of openai api code to original library syntax, since we don't install the private libraries */
function mapBackKeywords(modelAnswer, keywordMappings) {
    // Reverse the keyword mappings to map back to the original keywords
    const reverseMapping = Object.fromEntries(
        Object.entries(keywordMappings).map(([key, value]) => [value, key])
    );

    // Sort the reverse mapping by key length in descending order to avoid partial replacements
    const sortedMapping = Object.keys(reverseMapping).sort((a, b) => b.length - a.length);

    // Replace keywords in the model's answer
    let originalCode = modelAnswer;
    sortedMapping.forEach(privateKeyword => {
        const originalKeyword = reverseMapping[privateKeyword];
        originalCode = originalCode.split(privateKeyword).join(originalKeyword);
    });

    return originalCode;
}


/**Read key_words for Lodash Library */
const keywordMappingsDanfo = JSON.parse(fs.readFileSync('./apiDocumentation/danfo-JS/danfo_map_keywords.json', 'utf8'))
const danfyBM = JSON.parse(fs.readFileSync('./benchmarks/sample_danfy_private.json', 'utf8'))
const danfyDoc = JSON.parse(fs.readFileSync('./apiDocumentation/danfo-JS/danfy_private_doc.json', 'utf8'))

/**extract required file for Lodash private version (toolkit) */
const keywordMappingsLodash = JSON.parse(fs.readFileSync('./apiDocumentation/lodash/lodash_keywords.json', 'utf8'))
const toolkitBM = JSON.parse(fs.readFileSync('./benchmarks/toolkitBM.json', 'utf8'))
const toolDoc = JSON.parse(fs.readFileSync('./apiDocumentation/lodash/toolkit_doc.json', 'utf8'))

// Extract the prompts from the benchmarks
const danfy_prompts = danfyBM.benchmarks.map(bm => bm.prompt)

const toolkit_prompts = toolkitBM.benchmarks.map(tk => tk.prompt)


const fullPromptDanfy = {
    'api_documentation': danfyDoc,
    'benchmarks': danfy_prompts
};

const fullPromptToolkit = {
    'api_documentation': toolDoc,
    'benchmarks': toolkit_prompts
};

function testGPT_4mini(fullPrompt, mapList, benchmarks) {
    openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
            {
                role: "system",
                content: "You will recieve api_documentation for private library (JavaScript library), and benchmarks as JSON format. the benchmarks will consist of array of prompts, each prompt contain function signature (name and parameters) and must complete the body of the function based on the description in the prompt. the goal to test your performance to complete the function body using private library (based on the documentation you will get). your response should be in JSON format, contain array each index has the completion for the function body with it's signature only (no explation or instructions). please response only with json format containing the functions, no explanition or documentation needed, so i can parse it easily in my code. here how you response should look like: {'answers': ['def add_zeros_to_string(kf, col_name):\n    kf[col_name] = kf[col_name]. employ(lambda x: '{0:0>15}'.format(x))\n    return kf', 'def add_zeros(nums):\n    nums. map(lambda x: '{0:0>15}'.format(x))\n    return nums']}, if you recieved 2 benchmarks. and don't make any import within your function"
            },
            {
                role: "user",
                content: JSON.stringify(fullPrompt),
            },
        ],
    })
        .then(res => {
            //if the GPT answer, then run tests the answers
            let countCorr = 0
            //console.log(res.choices[0].message.content);

            const parse_ans = JSON.parse(res.choices[0].message.content)
            const all_ans = parse_ans.answers
            //console.log(all_ans);
            
            //now loop over the answers and run the proper test, to check correctnes of the code
            for (let i = 0; i < all_ans.length; i++) {
                const func = all_ans[i]

                const original_func = mapBackKeywords(func, mapList)
                //console.log(original_func);
                
                const test_code = benchmarks.benchmarks[i].test

                try {
                    eval(original_func)
                    eval(test_code)

                    // Extract function name
                    const functionName = original_func.split(' ')[1].split('(')[0];
                    const res = eval(`check(${functionName})`);

                    //console.log(res + ` ${functionName} \n`);
                    
                    if (res){
                        countCorr++
                    }
                }catch (error){
                    console.log(`An error occurred: ${error}`);
                    //console.log(error);
                    
                }
            }
            console.log(`Answers Correct: ${countCorr}`);
            
        })
        .catch((error) => {
            console.error(error.message);
        });
}

testGPT_4mini(fullPromptDanfy, keywordMappingsDanfo, danfyBM)
testGPT_4mini(fullPromptToolkit, keywordMappingsLodash, toolkitBM)








// Example usage
// let modelAnswer = `
// function mergeDataBoards(db1, db2, key) {
//     return danfy.combine({left: db1, right: db2, on: [key], how: 'inner'});
// }
// `;

// // Map the answer back to the original keywords
// const originalCode = mapBackKeywords(modelAnswer, keywordMappingsDanfo);
// // console.log(originalCode);

// const test_text = danfyBM['benchmarks'][0].test
// // console.log(test_text);

// eval(originalCode)
// eval(test_text)


// check(mergeDataFrames)