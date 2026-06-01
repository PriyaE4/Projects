// // import {useEffect,useState} from "react"
// // import axios from "axios"

// // import Navbar from "../Navbar"
// // import NoticeCard from "../NoticeCard"
// // import NoticeTicker from "../NoticeTicker"
// // import PostNotice from "./PostNotice"

// // function FacultyDashboard(){

// // const [notices,setNotices] = useState([])

// // useEffect(()=>{

// // axios.get("http://localhost:5000/api/notices/all")
// // .then(res=>setNotices(res.data))

// // },[])

// // return(

// // <div>

// // <Navbar/>

// // <NoticeTicker notices={notices}/>

// // <h2>Faculty Dashboard</h2>

// // <PostNotice/>

// // <h3>All Notices</h3>

// // {notices.map(n => (

// // <NoticeCard notice={n}/>

// // ))}

// // </div>

// // )

// // }

// // export default FacultyDashboard

// import { useEffect, useState } from "react";
// import axios from "axios";

// import Navbar from "../../components/Navbar/Navbar";
// import NoticeCard from "../../components/Notice/NoticeCard";
// import NoticeTicker from "../../components/Notice/NoticeTicker";
// import PostNotice from "../PostNotice";

// function FacultyDashboard(){

// const [notices,setNotices] = useState([]);

// useEffect(()=>{

// fetchNotices();

// },[]);


// const fetchNotices = async () => {

// try{

// const res = await axios.get(
// "http://localhost:5000/api/notices/all"
// );

// setNotices(res.data);

// }catch(err){

// console.log(err);

// }

// };


// return(

// <div>

// <Navbar/>

// <NoticeTicker notices={notices}/>

// <h2 style={{textAlign:"center"}}>
// Faculty Dashboard
// </h2>


// <PostNotice refreshNotices={fetchNotices}/>


// <h3 style={{marginLeft:"20px"}}>
// All Notices
// </h3>


// <div style={{

// display:"grid",
// gridTemplateColumns:"repeat(3,1fr)",
// gap:"20px",
// padding:"20px"

// }}>

// {notices.length === 0 ? (

// <h3>No notices available</h3>

// ):( 

// notices.map(n => (

// <NoticeCard key={n._id} notice={n}/>

// ))

// )}

// </div>


// </div>

// );

// }

// export default FacultyDashboard;
import {useEffect,useState} from "react"
import {getNotices} from "../../services/api"

import Navbar from "../../components/Navbar/Navbar"
import NoticeCard from "../../components/Notice/NoticeCard"
import PostNotice from "./PostNotice"
import ManageCoordinators from "./ManageCoordinators"

function FacultyDashboard(){

const [notices,setNotices] = useState([])
const [tab,setTab] = useState("notices")

useEffect(()=>{

let alive = true

const tick = async()=>{
try{
const res = await getNotices()
if(alive) setNotices(res.data)
}
catch(err){
console.log("Error fetching notices",err)
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

try{

const res = await getNotices()
setNotices(res.data)

}
catch(err){

console.log("Error fetching notices",err)

}

}

return(

<div>

<Navbar/>

<h2 style={{textAlign:"center"}}>
Faculty Dashboard
</h2>

{/* TAB BUTTONS */}

<div style={styles.tabs}>

<button
style={tab==="notices"?styles.activeTab:styles.tab}
onClick={()=>setTab("notices")}
>
Notices
</button>

<button
style={tab==="permissions"?styles.activeTab:styles.tab}
onClick={()=>setTab("permissions")}
>
Permissions
</button>

</div>

{/* TAB CONTENT */}

{tab==="notices" && (

<div>

{/* POST NOTICE */}

<PostNotice refreshNotices={fetchNotices}/>

<h3 style={{marginLeft:"20px"}}>
All Notices
</h3>

<div style={styles.grid}>

{notices.length===0 ? (

<p>No notices available</p>

):( 

notices.map(n => (

<NoticeCard
key={n._id}
notice={n}
refreshNotices={fetchNotices}
/>

))

)}

</div>

</div>

)}

{/* PERMISSIONS TAB */}

{tab==="permissions" && (

<ManageCoordinators/>

)}

</div>

)

}

const styles={

tabs:{
display:"flex",
justifyContent:"center",
gap:"20px",
margin:"20px"
},

tab:{
padding:"10px 20px",
border:"1px solid #ccc",
background:"white",
cursor:"pointer",
borderRadius:"6px"
},

activeTab:{
padding:"10px 20px",
border:"none",
background:"#2f80ed",
color:"white",
cursor:"pointer",
borderRadius:"6px"
},

grid:{
display:"grid",
gridTemplateColumns:"repeat(auto-fill,minmax(250px,1fr))",
gap:"20px",
padding:"20px"
}

}

export default FacultyDashboard
