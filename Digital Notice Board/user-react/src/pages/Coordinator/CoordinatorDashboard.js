// import {useEffect,useState} from "react"
// import axios from "axios"

// import Navbar from "../../components/Navbar/Navbar"
// import NoticeTicker from "../../components/Notice/NoticeTicker"
// import NoticeCard from "../../components/Notice/NoticeCard"
// import PostNotice from "../Faculty/PostNotice"

// function CoordinatorDashboard(){

// const [notices,setNotices] = useState([])

// useEffect(()=>{

// axios.get("http://localhost:5000/api/notices/all")
// .then(res=>setNotices(res.data))

// },[])

// return(

// <div>

// <Navbar/>

// <NoticeTicker notices={notices}/>

// <h2>Coordinator Dashboard</h2>

// <PostNotice/>

// {notices.map(n => (

// <NoticeCard notice={n}/>

// ))}

// </div>

// )

// }

// export default CoordinatorDashboard
import {useEffect,useState} from "react"
import {getNotices} from "../../services/api"

import Navbar from "../../components/Navbar/Navbar"
import NoticeTicker from "../../components/Notice/NoticeTicker"
import NoticeCard from "../../components/Notice/NoticeCard"
import PostNotice from "../Faculty/PostNotice"

function CoordinatorDashboard(){

const [notices,setNotices] = useState([])

useEffect(()=>{

let alive = true

const tick = async()=>{
try{
const res = await getNotices()
if(alive) setNotices(res.data)
}
catch(err){
console.log("Error loading notices",err)
}
}

tick()
const interval = setInterval(tick, 10000)

return ()=>{
alive = false
clearInterval(interval)
}

},[])

const fetchNotices = async()=>{
const res = await getNotices()
setNotices(res.data)
}

return(

<div>

<Navbar/>

{/* Scrolling Notice Bar */}

<NoticeTicker notices={notices}/>

<h2 style={{textAlign:"center",marginTop:"20px"}}>
Coordinator Dashboard
</h2>

{/* Post Notice Section */}

<PostNotice refreshNotices={fetchNotices}/>

{/* Notice Cards */}

<div style={styles.grid}>

{notices.map(n => (

<NoticeCard key={n._id} notice={n} refreshNotices={fetchNotices}/>

))}

</div>

</div>

)

}

const styles={

grid:{
display:"grid",
gridTemplateColumns:"repeat(auto-fill,minmax(250px,1fr))",
gap:"20px",
padding:"20px"
}

}

export default CoordinatorDashboard
