const app = require('express')()
const port = 8080

app.listen(
    port, () => {
        console.log(`It's alive on http://localhost:${port}`)
    }
)

app.get('/mozzart', async(req, res) => {
    function offersJsonToData(jsonData){
        let data = jsonData['matches']
        .map((match) => {
            return {
                id: match.id,
                participants: match.participants
            }
        })
        .filter((match) => match.participants.length > 1)
        .map((match) => {
            return {
                id: match.id,
                home: match.participants[0],
                away: match.participants[1],
            }
        })

        return data
    }

    let offersResponse = await fetch('http://localhost:8000/' + 'https://www.mozzartbet.com/betOffer2', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json',
                    "X-Requested-With": "XMLHttpRequest"},
        body: JSON.stringify(
            {
                date:"three_days",
                sportIds:[1],
                competitionIds:[],
                sort:"bycompetition",
                specials:false,
                subgames:[],
                size:1000,
                mostPlayed:false,
                type:"betting",
                numberOfGames:115,
                activeCompleteOffer:false,
                lang:"sr",
                offset:0
            }
        )
    });
    let offersData = offersJsonToData(await offersResponse.json())

    let result = await Promise.all(offersData.map(async (match, index) => {
        let oddsResponse = await fetch('http://localhost:8000/' + 'https://www.mozzartbet.com/matchBetting', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',
                        "X-Requested-With": "XMLHttpRequest"},
            body: JSON.stringify({
                id: match.id
            })
        });
        let matchOdds = (await oddsResponse.json())['kodds']

        let subGameOdds = {
            pairs: [
                {"1": null,"x": null, "2": null},
                {"1x": null, "2": null},
                {"12": null, "x": null},
                {"1": null, "x2": null},
                {"0-1": null, "2+": null},
                {"0-2": null, "3+": null},
                {"0-3": null, "4+": null},
                {"0-4": null, "5+": null},
                {"fh1": null,"fhx": null, "fh2": null},
                {"fh1x": null, "fh2": null},
                {"fh12": null, "fhx": null},
                {"fh1": null, "fhx2": null},
                {"fh0-1": null, "fh2+": null},
                {"sh1": null,"shx": null, "sh2": null},
                {"sh0-1": null, "sh2+": null},
            ]
        }
        subGameOdds.pairs[0]['1'] =      matchOdds['1001001001'] === undefined || matchOdds['1001001001'] === null ? null : matchOdds['1001001001'].value 
        subGameOdds.pairs[0]['x'] =      matchOdds['1001001002'] === undefined || matchOdds['1001001002'] === null ? null : matchOdds['1001001002'].value 
        subGameOdds.pairs[0]['2'] =      matchOdds['1001001003'] === undefined || matchOdds['1001001003'] === null ? null : matchOdds['1001001003'].value
 
        subGameOdds.pairs[1]["1x"] =     matchOdds['1001002001'] === undefined || matchOdds['1001002001'] === null ? null : matchOdds['1001002001'].value 
        subGameOdds.pairs[1]["2"] =      matchOdds['1001001003'] === undefined || matchOdds['1001001003'] === null ? null : matchOdds['1001001003'].value
         
        subGameOdds.pairs[2]["12"] =     matchOdds['1001002002'] === undefined || matchOdds['1001002002'] === null ? null : matchOdds['1001002002'].value 
        subGameOdds.pairs[2]["x"] =      matchOdds['1001001002'] === undefined || matchOdds['1001001002'] === null ? null : matchOdds['1001001002'].value
          
        subGameOdds.pairs[3]["1"] =      matchOdds['1001001001'] === undefined || matchOdds['1001001001'] === null ? null : matchOdds['1001001001'].value 
        subGameOdds.pairs[3]["x2"] =     matchOdds['1001002003'] === undefined || matchOdds['1001002003'] === null ? null : matchOdds['1001002003'].value
          
        subGameOdds.pairs[4]["0-1"] =    matchOdds['1001003001'] === undefined || matchOdds['1001003001'] === null ? null : matchOdds['1001003001'].value 
        subGameOdds.pairs[4]["2+"] =     matchOdds['1001003012'] === undefined || matchOdds['1001003012'] === null ? null : matchOdds['1001003012'].value
          
        subGameOdds.pairs[5]["0-2"] =    matchOdds['1001003002'] === undefined || matchOdds['1001003002'] === null ? null : matchOdds['1001003002'].value 
        subGameOdds.pairs[5]["3+"] =     matchOdds['1001003004'] === undefined || matchOdds['1001003004'] === null ? null : matchOdds['1001003004'].value
          
        subGameOdds.pairs[6]["0-3"] =    matchOdds['1001003013'] === undefined || matchOdds['1001003013'] === null ? null : matchOdds['1001003013'].value 
        subGameOdds.pairs[6]["4+"] =     matchOdds['1001003005'] === undefined || matchOdds['1001003005'] === null ? null : matchOdds['1001003005'].value
          
        subGameOdds.pairs[7]["0-4"] =    matchOdds['1001003026'] === undefined || matchOdds['1001003026'] === null ? null : matchOdds['1001003026'].value 
        subGameOdds.pairs[7]["5+"] =     matchOdds['1001003007'] === undefined || matchOdds['1001003007'] === null ? null : matchOdds['1001003007'].value
          
        subGameOdds.pairs[8]["fh1"] =    matchOdds['1001004001'] === undefined || matchOdds['1001004001'] === null ? null : matchOdds['1001004001'].value 
        subGameOdds.pairs[8]["fhx"] =    matchOdds['1001004002'] === undefined || matchOdds['1001004002'] === null ? null : matchOdds['1001004002'].value 
        subGameOdds.pairs[8]["fh2"] =    matchOdds['1001004003'] === undefined || matchOdds['1001004003'] === null ? null : matchOdds['1001004003'].value
          
        subGameOdds.pairs[9]["fh1x"] =   matchOdds['1001297001'] === undefined || matchOdds['1001297001'] === null ? null : matchOdds['1001297001'].value 
        subGameOdds.pairs[9]["fh2"] =    matchOdds['1001004003'] === undefined || matchOdds['1001004003'] === null ? null : matchOdds['1001004003'].value
         
        subGameOdds.pairs[10]["fh12"] =  matchOdds['1001297002'] === undefined || matchOdds['1001297002'] === null ? null : matchOdds['1001297002'].value 
        subGameOdds.pairs[10]["fhx"] =   matchOdds['1001004002'] === undefined || matchOdds['1001004002'] === null ? null : matchOdds['1001004002'].value
         
        subGameOdds.pairs[11]["fh1"] =   matchOdds['1001004001'] === undefined || matchOdds['1001004001'] === null ? null : matchOdds['1001004001'].value 
        subGameOdds.pairs[11]["fhx2"] =  matchOdds['1001297003'] === undefined || matchOdds['1001297003'] === null ? null : matchOdds['1001297003'].value
        
        subGameOdds.pairs[12]["fh0-1"] = matchOdds['1001008005'] === undefined || matchOdds['1001008005'] === null ? null : matchOdds['1001008005'].value 
        subGameOdds.pairs[12]["fh2+"] =  matchOdds['1001008002'] === undefined || matchOdds['1001008002'] === null ? null : matchOdds['1001008002'].value
        
        subGameOdds.pairs[13]["sh1"] =   matchOdds['1001019001'] === undefined || matchOdds['1001019001'] === null ? null : matchOdds['1001019001'].value 
        subGameOdds.pairs[13]["shx"] =   matchOdds['1001019002'] === undefined || matchOdds['1001019002'] === null ? null : matchOdds['1001019002'].value 
        subGameOdds.pairs[13]["sh2"] =   matchOdds['1001019003'] === undefined || matchOdds['1001019003'] === null ? null : matchOdds['1001019003'].value
        
        subGameOdds.pairs[14]["sh0-1"] = matchOdds['1001009005'] === undefined || matchOdds['1001009005'] === null ? null : matchOdds['1001009005'].value 
        subGameOdds.pairs[14]["sh2+"] =  matchOdds['1001009002'] === undefined || matchOdds['1001009002'] === null ? null : matchOdds['1001009002'].value

        offersData[index]['subGameOdds'] = subGameOdds

        console.log(`Processed ${index+1}/${offersData.length} matches.`)
        return offersData[index]
    }))

    res.status(202).send(result)
})