
let currentPage = 1;
let pageSize = 10;
let selectedIds = [];

document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
});

function loadProducts() {
    const tbody = document.getElementById('commissionTable');
    tbody.innerHTML = '<tr><td colspan="9" class="text-center">加载中...</td></tr>';
    
    const params = new URLSearchParams(window.location.search);
    const keyword = params.get('keyword') || '';
    
    fetch(`/api/product/list/admin?page=${currentPage}&page_size=${pageSize}&keyword=${keyword}`)
        .then(res => res.json())
        .then(res => {
            if (res.code === 200) {
                renderTable(res.data.list);
                renderPagination(res.data.total);
            } else {
                const tbody = document.getElementById('commissionTable');
                tbody.innerHTML = `<tr><td colspan="9" class="text-center text-danger">加载失败: ${res.message || '未知错误'}</td></tr>`;
            }
        })
        .catch(err => {
            const tbody = document.getElementById('commissionTable');
            tbody.innerHTML = `<tr><td colspan="9" class="text-center text-danger">网络错误: ${err.message}</td></tr>`;
        });
}

function renderTable(list) {
    const tbody = document.getElementById('commissionTable');
    if (!list || list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center">暂无数据</td></tr>';
        return;
    }
    
    const settlementMap = {1: '月结', 2: '周结', 3: '实时'};
    
    tbody.innerHTML = list.map(item => `
        <tr>
            <td><input type="checkbox" class="product-check" value="${item.id}" ${selectedIds.includes(item.id) ? 'checked' : ''}></td>
            <td>${item.id}</td>
            <td>
                <div style="max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${item.name}">
                    ${item.name}
                </div>
            </td>
            <td><span class="badge badge-primary">${item.commission_rate}%</span></td>
            <td><span class="badge badge-info">${item.normal_rate}%</span></td>
            <td><span class="badge badge-success">${item.premium_rate}%</span></td>
            <td><span class="badge badge-warning">${item.top_rate}%</span></td>
            <td>${settlementMap[item.settlement_type] || '月结'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editCommission(${item.id})">编辑</button>
            </td>
        </tr>
    `).join('');
}

function renderPagination(total) {
    const totalPages = Math.ceil(total / pageSize);
    const ul = document.getElementById('pagination');
    let html = '';
    
    if (currentPage > 1) {
        html += `<li class="page-item"><a class="page-link" href="javascript:void(0)" onclick="goPage(${currentPage - 1})">上一页</a></li>`;
    }
    
    for (let i = 1; i <= totalPages; i++) {
        if (i === currentPage) {
            html += `<li class="page-item active"><a class="page-link" href="javascript:void(0)">${i}</a></li>`;
        } else {
            html += `<li class="page-item"><a class="page-link" href="javascript:void(0)" onclick="goPage(${i})">${i}</a></li>`;
        }
    }
    
    if (currentPage < totalPages) {
        html += `<li class="page-item"><a class="page-link" href="javascript:void(0)" onclick="goPage(${currentPage + 1})">下一页</a></li>`;
    }
    
    ul.innerHTML = html;
}

function goPage(page) {
    currentPage = page;
    loadProducts();
}

function editCommission(id) {
    fetch(`/api/product/list/admin?page=1&page_size=100`)
        .then(res => res.json())
        .then(res => {
            if (res.code === 200) {
                const item = res.data.list.find(p => p.id === id);
                if (item) {
                    document.getElementById('productId').value = item.id;
                    document.getElementById('productName').value = item.name;
                    document.getElementById('commissionRate').value = item.commission_rate;
                    document.getElementById('normalRate').value = item.normal_rate;
                    document.getElementById('premiumRate').value = item.premium_rate;
                    document.getElementById('topRate').value = item.top_rate;
                    document.getElementById('settlementType').value = item.settlement_type;
                    $('#commissionModal').modal('show');
                }
            }
        });
}

function saveCommission() {
    const id = document.getElementById('productId').value;
    const data = {
        commission_rate: parseFloat(document.getElementById('commissionRate').value),
        normal_rate: parseFloat(document.getElementById('normalRate').value),
        premium_rate: parseFloat(document.getElementById('premiumRate').value),
        top_rate: parseFloat(document.getElementById('topRate').value),
        settlement_type: parseInt(document.getElementById('settlementType').value)
    };
    
    fetch(`/api/product/commission/update/${id}`, {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    }).then(res => res.json()).then(res => {
        if (res.code === 200) {
            $('#commissionModal').modal('hide');
            loadProducts();
        } else {
            alert(res.message || '保存失败');
        }
    });
}

function batchUpdate() {
    const checkboxes = document.querySelectorAll('.product-check:checked');
    selectedIds = Array.from(checkboxes).map(cb => parseInt(cb.value));
    
    if (selectedIds.length === 0) {
        alert('请先选择商品');
        return;
    }
    
    document.getElementById('selectedCount').innerText = selectedIds.length;
    $('#batchModal').modal('show');
}

function saveBatch() {
    const data = {};
    const fields = ['commission_rate', 'normal_rate', 'premium_rate', 'top_rate'];
    const prefix = 'batch';
    
    fields.forEach(field => {
        const value = parseFloat(document.getElementById(prefix + field.charAt(0).toUpperCase() + field.slice(1)).value);
        if (!isNaN(value)) {
            data[field] = value;
        }
    });
    
    if (Object.keys(data).length === 0) {
        alert('请至少填写一个佣金比例');
        return;
    }
    
    fetch('/api/product/commission/batch-update', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ids: selectedIds, ...data})
    }).then(res => res.json()).then(res => {
        if (res.code === 200) {
            $('#batchModal').modal('hide');
            selectedIds = [];
            loadProducts();
        } else {
            alert(res.message || '批量保存失败');
        }
    }).catch(err => {
        alert('批量保存失败');
    });
}

function exportCommission() {
    window.location.href = '/api/product/commission/export';
}

document.getElementById('checkAll').addEventListener('change', function() {
    document.querySelectorAll('.product-check').forEach(cb => cb.checked = this.checked);
    if (this.checked) {
        fetch(`/api/product/list/admin?page=1&page_size=1000`)
            .then(res => res.json())
            .then(res => {
                if (res.code === 200) {
                    selectedIds = res.data.list.map(p => p.id);
                }
            });
    } else {
        selectedIds = [];
    }
});
