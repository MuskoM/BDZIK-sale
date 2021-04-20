
let closeNavbar = () => {
    let sidebar = document.getElementById("sidebar-class-planner")
    sidebar.style.visibility = "hidden"
    sidebar.style.width = "0px"
    let sidebar_arrow = document.getElementsByClassName("list-group-hide-control").item(0)
    sidebar_arrow.addEventListener('click',()=>openNavbar())
}

let openNavbar = () => {
    let sidebar = document.getElementById("sidebar-class-planner")
    sidebar.style.visibility = "visible"
    sidebar.style.width = "250px"
    let sidebar_arrow = document.getElementsByClassName("list-group-hide-control").item(0)
    sidebar_arrow.addEventListener('click',()=>closeNavbar())

}

   closeNavbar()