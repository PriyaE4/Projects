// import { useEffect, useState } from "react";
// import axios from "axios";
// import Navbar from "../../components/Navbar/Navbar";

// function Profile() {

// const [user,setUser] = useState({});
// const userId = localStorage.getItem("userId");

// useEffect(()=>{

// axios.get(`http://localhost:5000/api/users/profile/${userId}`)
// .then(res=>setUser(res.data))
// .catch(err=>console.log(err));

// },[]);

// return(

// <div>

// <Navbar/>

// <h2 style={{textAlign:"center"}}>My Profile</h2>

// <div style={{
// width:"400px",
// margin:"auto",
// border:"1px solid #ddd",
// padding:"20px",
// borderRadius:"10px"
// }}>

// <p><b>Name:</b> {user.name}</p>
// <p><b>Username:</b> {user.username}</p>
// <p><b>Email:</b> {user.email}</p>
// <p><b>Phone:</b> {user.phoneNumber}</p>
// <p><b>Branch:</b> {user.branch}</p>
// <p><b>Roll:</b> {user.rollNumber}</p>

// <a href="/edit-profile">Edit Profile</a>

// </div>

// </div>

// );

// }

// export default Profile;
import {useEffect,useState} from "react"
import {getProfile} from "../../services/api"

import Navbar from "../../components/Navbar/Navbar"
import {useNavigate} from "react-router-dom"

function Profile(){

const [user,setUser] = useState({})
const [loading,setLoading] = useState(true)

const navigate = useNavigate()
const userId = localStorage.getItem("userId")

useEffect(()=>{

fetchProfile()

},[])

const fetchProfile = async()=>{

try{

const res = await getProfile(userId)
setUser(res.data)

}catch(err){

console.log("Error loading profile")

}

setLoading(false)

}

if(loading){
return(
<div>
<Navbar/>
<h3 style={{textAlign:"center"}}>Loading Profile...</h3>
</div>
)
}

return(

<div>

<Navbar/>

<div style={styles.card}>

<h2 style={{textAlign:"center"}}>My Profile</h2>

<div style={styles.info}>
<p><b>Name:</b> {user.name}</p>
<p><b>Username:</b> {user.username}</p>
<p><b>Email:</b> {user.email}</p>
<p><b>Phone:</b> {user.phoneNumber}</p>

{user.branch && <p><b>Branch:</b> {user.branch}</p>}
{user.rollNumber && <p><b>Roll Number:</b> {user.rollNumber}</p>}
{user.role && <p><b>Role:</b> {user.role}</p>}
</div>

<button
style={styles.button}
onClick={()=>navigate("/edit-profile")}
>
Edit Profile
</button>

</div>

</div>

)

}

const styles={

card:{
width:"420px",
margin:"60px auto",
padding:"30px",
background:"white",
borderRadius:"10px",
boxShadow:"0px 8px 20px rgba(0,0,0,0.1)"
},

info:{
lineHeight:"1.8",
marginBottom:"20px"
},

button:{
width:"100%",
padding:"12px",
background:"#2f80ed",
color:"white",
border:"none",
borderRadius:"6px",
cursor:"pointer",
fontSize:"16px"
}

}

export default Profile