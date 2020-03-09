import React, {useState, useEffect, Text} from 'react'
import axios from 'axios'
import Quote from './Quote/index'


function App() {
    const [numreg, setReg] = useState(0);
    const [numrst, setRst] = useState(0);
    const [old, setOldest] = useState(0);
    const [first, setFirst] = useState(0);
    const [time, setTime] = useState(0);


    const CountValues=()=> {
        axios.get('http://localhost:8100/events/stats')
          .then(json => {  
            console.log(json)
              setReg(json.data["num_region_stats"])
              setRst(json.data['num_roast_stats'])
          })
      }
    
    const OldestRoast=()=> {
        axios.get('http://localhost:8120/log/roast')
          .then(json => {
            setOldest(JSON.stringify(json.data.payload))
          })
      }
    
    const NewestRegion=()=> {
        axios.get('http://localhost:8120/log/region?offset=1')
          .then(json => {
            setFirst(JSON.stringify(json.data.payload))
          })
      }
    
    const getData=()=>{
        let d = Date()
        console.log(d)
        setTime(d)
        CountValues()
        OldestRoast()
        NewestRegion()

    }
    
    useEffect(()=>{
        //setInterval(getData, 5000)
        setTimeout(getData, 5000)
    })


    return(
            <div style={{border:"2px black solid"}}>
            <p>Number of recorded regions</p>
            <p>{numreg}</p>
            <p>Number of recorded roasts</p>
            <p>{numrst}</p>
            <p>Oldest roast recorded</p>
            <p>{old}</p>
            <p>Newest Region recorded</p>
            <p>{first}</p>
            <p>Last update</p>
            <p>{time}</p>
            </div>
    )
}

export default App