function downloadMp4(box_num, seed_num, id, url, type) {
    axios({
        url: url,
        method: 'GET',
        responseType: 'blob',
        headers: {'Content-Disposition': 'attachment'},
        onDownloadProgress: (progressEvent) => {
            let percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            document.getElementById(id).setAttribute('aria-valuenow', String(percentCompleted))
            document.getElementById(id).setAttribute('style','width:'+Number(percentCompleted)+'%')
        }
    }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${box_num}.${type}`);
        document.body.appendChild(link);
        link.click();
    });
}

function downloadTipCoords(box_num, seed_num, csrf_token) {
    axios({
        url: '/internal/',
        method: 'POST',
        responseType: 'json',
        headers: {'X-CSRFToken': csrf_token},
        data: {'box_num': String(box_num), 'seed_num': String(seed_num)}
    }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([JSON.stringify(response.data)], {type: "application/json"}));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${box_num}-${seed_num}.json`);
        document.body.appendChild(link);
        link.click();
    });
}