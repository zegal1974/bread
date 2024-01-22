

function getActors(start, page){
  console.log("getActors called with start: " + start + " and page: " + page)
  getActorsFromServer(start, page).then(response => {
    console.log("getActors response: " + response)
  })
  return []
}



export default { getActors }