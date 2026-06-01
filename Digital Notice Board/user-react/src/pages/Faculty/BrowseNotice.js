import {useEffect,useState} from "react"
import {getNotices} from "../../services/api"
import NoticeCard from "../../components/Notice/NoticeCard"

function BrowseNotice(){

const [notices,setNotices]=useState([])

useEffect(()=>{

getNotices().then(res=>setNotices(res.data))

},[])

return(

<div>

<h2>Browse Notices</h2>

{notices.map(n=>(
<NoticeCard key={n._id} notice={n}/>
))}

</div>

)

}

export default BrowseNotice