import { useEffect, useState } from "react"

export default function Mozzart(){
    const [matches, setMatches] = useState([])

    function jsonToData(jsonData){
        setMatches(jsonData['matches']
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
        }))
    }

    useEffect(() => {
        fetch('https://corsproxy.io/?' + encodeURIComponent('https://www.mozzartbet.com/betOffer2'), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json',
                        'sec-fetch-dest':'empty',
                        'sec-fetch-mode':'cors',
                        'sec-fetch-site':'same-origin', },
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
        }).then(response => response.json()).then(data => jsonToData(data));
    }, [])

    return <>
        {matches.map(match => {
            return <>
                <div className="grid grid-cols-3 w-1/2">
                    <h2>{match.id}</h2>
                    <h2>{match.home.name}</h2>
                    <h2>{match.away.name}</h2>
                </div>
            </>
        })}
    </>
}