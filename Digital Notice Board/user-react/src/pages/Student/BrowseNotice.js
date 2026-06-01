// import { useEffect, useState } from "react";
// import { getNotices } from "../../services/api";

// import Navbar from "../../components/Navbar/Navbar";
// import NoticeCard from "../../components/Notice/NoticeCard";

// function BrowseNotice(){

// const [notices,setNotices] = useState([]);

// useEffect(()=>{

// getNotices()
// .then(res=>setNotices(res.data))
// .catch(err=>console.log(err));

// },[]);

// return(

// <div>

// <Navbar/>

// <h2 style={{textAlign:"center"}}>
// Browse Notices
// </h2>

// <div style={{

// display:"grid",
// gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))",
// gap:"20px",
// padding:"20px"

// }}>

// {notices.map(n=>(
// <NoticeCard key={n._id} notice={n}/>
// ))}

// </div>

// </div>

// );

// }

// export default BrowseNotice;
import { useEffect, useState } from "react";
import { getNotices } from "../../services/api";

import Navbar from "../../components/Navbar/Navbar";
import NoticeCard from "../../components/Notice/NoticeCard";

function BrowseNotice(){

const [notices,setNotices] = useState([]);
const [loading,setLoading] = useState(true);

useEffect(()=>{

fetchNotices();

},[]);

const fetchNotices = async()=>{

try{

const res = await getNotices();
setNotices(res.data);

}catch(err){

console.log(err);

}

setLoading(false);

};

return(

<div>

<Navbar/>

<h2 style={{textAlign:"center"}}>
Browse Notices
</h2>

{loading ? (

<h3 style={{textAlign:"center"}}>
Loading notices...
</h3>

) : (

<div style={styles.grid}>

{notices.length === 0 ? (

<p style={{textAlign:"center"}}>
No notices available
</p>

) : (

notices.map(n => (
<NoticeCard key={n._id} notice={n}/>
))

)}

</div>

)}

</div>

);

}

const styles = {

grid:{
display:"grid",
gridTemplateColumns:"repeat(auto-fit,minmax(300px,1fr))",
gap:"20px",
padding:"20px"
}

};

export default BrowseNotice;
