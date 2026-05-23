
// 通用请求封装
async function requestApi(url, data, method="GET"){
    const baseUrl = "/api" + url;
    let options = {headers:{"Content-Type":"application/json"}};
    if(method === "POST"){
        options.method = "POST";
        options.body = JSON.stringify(data);
    }else if(Object.keys(data).length > 0){
        const params = new URLSearchParams(data);
        url = baseUrl + "?" + params.toString();
    }else{
        url = baseUrl;
    }
    const res = await fetch(url, options);
    return await res.json();
}

// 新增项目
async function addNewProject(){
    const name = document.getElementById("projName").value.trim();
    const gitUrl = document.getElementById("gitAddr").value.trim();
    if(!name || !gitUrl){
        alert("项目名称和仓库地址不能为空！");
        return;
    }
    const result = await requestApi("/project/add", {name, url:gitUrl}, "POST");
    alert(result.msg);
    renderProjectList();
    // 清空输入框
    document.getElementById("projName").value = "";
    document.getElementById("gitAddr").value = "";
}

// 渲染项目列表
async function renderProjectList(){
    const res = await requestApi("/project/list", {});
    let htmlStr = "";
    res.data.forEach(item => {
        htmlStr += `
        <div class="project-item">
            <div class="info-text">
                <p>${item.name}</p>
                <span>仓库地址：${item.git_url}</span>
                <span>处理状态：${item.status}</span>
            </div>
            <button class="btn btn-del" onclick="removeProject(${item.id})">删除</button>
        </div>
        `;
    });
    document.getElementById("projectList").innerHTML = htmlStr;
}

// 删除项目
async function removeProject(id){
    if(!confirm("确认删除该项目，缓存文件将一并清除？")) return;
    await requestApi("/project/del", {id}, "POST");
    renderProjectList();
}

// 页面加载初始化
window.onload = function(){
    renderProjectList();
}
