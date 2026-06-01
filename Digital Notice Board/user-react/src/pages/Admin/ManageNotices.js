import {useEffect,useState} from "react"
import Navbar from "../../components/Navbar/Navbar"
import NoticeCard from "../../components/Notice/NoticeCard"
import {getNotices} from "../../services/api"

function ManageNotices(){

const [notices,setNotices] = useState([])
const [error,setError] = useState("")

const fetchNotices = async()=>{

try{
setError("")
const res = await getNotices()
setNotices(res.data || [])
}
catch(err){
setError(String(err?.response?.data || err.message || "Failed to load notices"))
}

}

useEffect(()=>{
let alive = true

const tick = async()=>{
try{
setError("")
const res = await getNotices()
if(alive) setNotices(res.data || [])
}
catch(err){
if(alive) setError(String(err?.response?.data || err.message || "Failed to load notices"))
}
}

tick()
const interval = setInterval(tick, 10000)

return ()=>{
alive = false
clearInterval(interval)
}
},[])

return(

<div>

<Navbar/>

<div className="page-shell">
<div className="card">
<div className="dashboard-top">
<div>
<h2 style={{margin:"0 0 6px"}}>Manage Notices</h2>
<p className="subtitle">Edit, pin/unpin, or delete notices.</p>
</div>
</div>

{error ? <p className="error-text">{error}</p> : null}

<div className="notice-list">
{notices.length===0 ? (
<p className="muted-text">No notices available.</p>
) : (
notices.map(n=>(
<NoticeCard
key={n._id}
notice={n}
refreshNotices={fetchNotices}
/>
))
)}
</div>

</div>
</div>

</div>

)

}

export default ManageNotices
