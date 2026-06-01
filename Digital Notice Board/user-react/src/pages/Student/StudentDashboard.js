// import { useEffect, useState } from "react";
// import axios from "axios";
// import Navbar from "../components/Navbar/Navbar";
// import NoticeCard from "../components/Notice/NoticeCard";

// function StudentDashboard(){

// const [notices,setNotices] = useState([]);

// useEffect(()=>{
// fetchNotices();
// },[]);

// const fetchNotices = async ()=>{

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

// <h1 style={{textAlign:"center"}}>
// Student Dashboard
// </h1>

// <div style={{
// display:"grid",
// gridTemplateColumns:"repeat(3,1fr)",
// gap:"20px",
// padding:"20px"
// }}>

// {notices.length===0 ? (

// <h2>No notices available</h2>

// ):( 

// notices.map((notice)=>(
// <NoticeCard key={notice._id} notice={notice}/>
// ))

// )}

// </div>

// </div>

// );

// }

// export default StudentDashboard;
// import { useEffect, useState } from "react";
// import axios from "axios";
// import Navbar from "../components/Navbar/Navbar";
// import NoticeCard from "../components/Notice/NoticeCard";

// function StudentDashboard(){

// const [notices,setNotices] = useState([]);

// useEffect(()=>{
// fetchNotices();
// },[]);

// const fetchNotices = async ()=>{

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

// <h1 style={{textAlign:"center"}}>
// Student Dashboard
// </h1>

// <div style={{
// display:"grid",
// gridTemplateColumns:"repeat(3,1fr)",
// gap:"20px",
// padding:"20px"
// }}>

// {notices.length===0 ? (

// <h2>No notices available</h2>

// ):( 

// notices.map((notice)=>(
// <NoticeCard key={notice._id} notice={notice}/>
// ))

// )}

// </div>

// </div>

// );

// }

// export default StudentDashboard;
import {useEffect,useState} from "react"
import {getNotices} from "../../services/api"

import Navbar from "../../components/Navbar/Navbar"
import NoticeCard from "../../components/Notice/NoticeCard"
import NoticeTicker from "../../components/Notice/NoticeTicker"

function StudentDashboard(){

const [notices,setNotices] = useState([])
const [error,setError] = useState("")

useEffect(()=>{

let alive = true

const fetchNotices = async()=>{
try{
setError("")
const res = await getNotices()
if(alive) setNotices(res.data)
}
catch(err){
console.log(err)
if(alive) setError(err?.response?.data?.message || "Failed to load notices")
}
}

fetchNotices()
const interval = setInterval(fetchNotices, 10000)

return ()=>{
alive = false
clearInterval(interval)
}

},[])

return(

<div>

<Navbar/>

<NoticeTicker notices={notices}/>

<h2 style={{textAlign:"center"}}>

Student Dashboard

</h2>

{error ? (
<p style={{textAlign:"center",color:"red"}}>
{error}
</p>
) : null}

<div style={{

display:"grid",
gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))",
gap:"20px",

padding:"20px"

}}>

{notices.map(n => (

<NoticeCard key={n._id} notice={n}/>

))}

</div>

</div>

)

}

export default StudentDashboard
