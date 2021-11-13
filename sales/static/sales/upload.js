const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value 
const alertBox = document.getElementById('alert-box')


const handleAlerts = (type, msg,title,color) => {
    alertBox.innerHTML = `
        <div class="alert ${type}">
        <h4 style="line-height: 160%"><span style="font-weight:700;color:${color}">${title}: </span> ${msg}</h4>
      </div>
    `
}
Dropzone.autoDiscover = false
const myDropzone = new Dropzone('#my-dropozne', {
    url: '/upload/',
    init: function() {
        this.on('sending', function(file, xhr, formData){
            console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function(file, response){
            console.log(response.ex)
            if(response.ex) {
                handleAlerts('danger-alert', 'File already exists','oops','#8f130c')

            } else {
                handleAlerts('success-alert', 'Your file has been uploaded','Good job','#178344')

            }
        })
    },
    maxFiles: 3,
    maxFilesize: 3,
    acceptedFiles: '.csv,.xlsx'
})


