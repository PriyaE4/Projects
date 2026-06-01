// function NoticeTicker({notices}){

// return(

// <div style={styles.ticker}>

// <marquee>

// {notices.map(n => n.title + " | ")}

// </marquee>

// </div>

// );

// }

// const styles = {

// ticker:{
// background:"#2f80ed",
// color:"white",
// padding:"10px",
// fontWeight:"bold"
// }

// };

// export default NoticeTicker;
import "./NoticeTicker.css"

function NoticeTicker({notices}){

if(!notices || notices.length === 0){
return null
}

const text = notices.map(n => n.title).join("  •  ")

return(

<div className="ticker-wrapper">

<div className="ticker">

<span>{text}</span>
<span>{text}</span>

</div>

</div>

)

}

export default NoticeTicker