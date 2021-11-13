const reportBtn = document.getElementById('report-btn')
const img = document.getElementById('img')
const modalBody = document.getElementById('modal-body')
const reportForm = document.getElementById('report-form')
const alertBox = document.getElementById('alert-box')

const reportName = document.getElementById('id_name')
const reportRemarks = document.getElementById('id_remarks')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value
const handleAlerts = (type, msg,title,color) => {
    alertBox.innerHTML = `
        <div class="alert ${type}">
        <h4 style="line-height: 160%"><span style="font-weight:700;color:${color}">${title}: </span> ${msg}</h4>
      </div>
    `
}

reportBtn.addEventListener('click', ()=>{
    console.log('clicked')
    img.setAttribute('class', 'w-100')
    img.setAttribute('class', 'h-40')
    img.setAttribute('class', 'd-none')
    modalBody.prepend(img)
    // console.log(img.src)

    reportForm.addEventListener('submit', e=>{
        e.preventDefault()
        const formData = new FormData()
        formData.append('csrfmiddlewaretoken', csrf)
        formData.append('name', reportName.value)
        formData.append('remarks', reportRemarks.value)
        formData.append('image', img.src)
        $.ajax({
            type: 'POST',
            url: '/reports/save/',
            data: formData,
            success: function(response){
                console.log(response)
                handleAlerts('success-alert', 'The chart has been created','Good job','#178344')
                reportForm.reset()
            },
            error: function(error){
                console.log(error)
                handleAlerts('danger-alert', 'You got an error','Error','#8f130c')
            },
            processData: false,
            contentType: false,
        })
    })
})