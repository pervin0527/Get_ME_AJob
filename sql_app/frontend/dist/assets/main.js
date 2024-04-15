
// 데이터 받아오기
function fetchData(db_name) {    
    return fetch(`http://127.0.0.1:8000/${db_name}`) // local에서 할 때 127.0.0.1으로 변경해야 됨!!
        .then(response => {

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        return response.json();
    })
    .catch(error => {
        console.error(`Error fetching ${db_name} data:`, error);
        return [];
    });
}

class App{
    constructor(db_data){
        this.db_data = db_data;
        console.log(this.db_data);

        this.c = document.querySelector('#myChart');
        this.cur_chart = null;
        this.cur_field = 'init';
        this.is_bar = true;
        
        //첫 화면 그래프 그리기
        this.drawPlot(this.cur_field, this.is_bar);

        // 옵션 누룰 때 마다 차트 변경
        this.search = document.querySelector('.search');
        this.search.addEventListener('change', (event)=>{
            this.cur_field = this.search.value;
            this.drawPlot(this.cur_field, this.is_bar);
        });

        // 바 하고 원 차트 변경

       
    }

    drawPlot(active_filed, is_bar){
        let x_labels = [];
        let y_labels = [];
        let related_skills;
        let title;

        // chart가 그려져 있으면 지우기
        if(this.cur_chart){
            this.cur_chart.destroy();
        }

        // 전체 분야 분포 그래프
        if(active_filed == 'init'){
            // init filed labels
            this.db_data.forEach(element => {
                const field = element['main_field'];
                const cnt = element['num_posts'];

                x_labels.push(field);
                y_labels.push(cnt);
            });

            if(is_bar){
                this.cur_chart = this.drawBarPlot(x_labels, y_labels, '인공지능 채용 분야 비중');
            }
            else{
                this.cur_chart = this.drawPiePlot(x_labels, y_labels, '인공지능 채용 분야 비중');
            }

            return;
        }

        // 컴퓨터 비전
        else if(active_filed == 'cv'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='컴퓨터 비전'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '컴퓨터 비젼 연관 기술';
        }

        //자연어 처리
        else if(active_filed == 'nlp'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='자연어 처리'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            
            title = '자연어 처리 연관 기술';
        }

        //데이터 엔지니어링
        else if(active_filed == 'data_engineer'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='데이터 엔지니어링'){
                    related_skills = element['related_field'];
                    break;
                }
            }

            title = '데이터 엔지니어링 연관 기술';
        }

        //백엔드 개발
        else if(active_filed == 'backend'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='백엔드 개발'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '백엔드 개발 연관 기술';
        }

        //프론트 엔드 개발
        else if(active_filed == 'frontend'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='프론트엔드 개발'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '프론트 엔드 연관 기술';
        }

        //보안
        else if(active_filed == 'security'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='보안'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '보안 연관 기술';
        }

        //금융
        else if(active_filed == 'finance'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='금융'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '금융 연관 기술';
        }

        //메타버스
        else if(active_filed == 'metavers'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='메타버스'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '메타버스 연관 기술';
        }

        //블록체인
        else if(active_filed == 'block_chain'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='블록체인'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '블록체인 연관 기술';
        }

        //시스템 개발
        else if(active_filed == 'system'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='시스템 개발'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '시스템 개발 연관 기술';
        }

        //모바일 개발
        else if(active_filed == 'mobile'){
            for(let i=0; i < this.db_data.length; i++){
                const element = this.db_data[i];

                if(element['main_field']=='모바일 개발'){
                    related_skills = element['related_field'];
                    break;
                }
            }
            title = '모바일 개발 연관 기술';
        }

        related_skills = related_skills.replace(/'/g, '"');
        related_skills = JSON.parse(related_skills);

        related_skills.forEach(element => {
            const skill_item = Object.entries(element);
            const skill = skill_item[0][0];
            const cnt = Number(skill_item[0][1]);
            x_labels.push(skill);
            y_labels.push(cnt);
        });

        if(is_bar){
            this.cur_chart = this.drawBarPlot(x_labels, y_labels, title);
        }
        else{
            this.cur_chart = this.drawPiePlot(x_labels, y_labels, title);
        }
    }

    drawPiePlot(x_labels, y_labels, title){
        const pie_data = {
            labels: x_labels,
            datasets: [{
              label: title,
              data: y_labels,
              borderWidth: 1,
              backgroundColor: ['#FF5733', '#33FF57','#337AFF', '#FF33E6', '#33FFC1', '#FFD133', '#CC33FF', '#FF337A', '#33FF91', '#FF5733', '#337AFF'],
            }]
        };

        const pie_config = {
            type: 'pie',
            data: pie_data,
            options: {
              plugins: {
                legend: {
                  onHover: this.handleHover,
                  onLeave: this.handleLeave
                }
              }
            }
        };

        return new Chart(this.c, pie_config);
    }
    
    handleLeave(evt, item, legend) {
        legend.chart.data.datasets[0].backgroundColor.forEach((color, index, colors) => {
          colors[index] = color.length === 9 ? color.slice(0, -2) : color;
        });
        legend.chart.update();
    }

    handleHover(evt, item, legend) {
        legend.chart.data.datasets[0].backgroundColor.forEach((color, index, colors) => {
          colors[index] = index === item.index || color.length === 9 ? color : color + '4D';
        });
        legend.chart.update();
    }

    drawBarPlot(x_labels, y_labels, title){
        const bar_data = {
            labels: x_labels,
            datasets: [{
                label: title,
                data: y_labels,
                backgroundColor: [
                    'rgba(255, 102, 102, 0.2)',
                    'rgba(255, 178, 102, 0.2)',
                    'rgba(255, 255, 102, 0.2)',
                    'rgba(178, 255, 102, 0.2)',
                    'rgba(102, 255, 102, 0.2)',
                    'rgba(102, 255, 178, 0.2)',
                    'rgba(102, 255, 255, 0.2)',
                    'rgba(102, 178, 255, 0.2)',
                    'rgba(102, 102, 255, 0.2)',
                    'rgba(178, 102, 255, 0.2)',
                    'rgba(255, 102, 255, 0.2)',
                ],
                borderColor: [
                    'rgb(255, 102, 102)',
                    'rgb(255, 178, 102)',
                    'rgb(255, 255, 102)',
                    'rgb(178, 255, 102)',
                    'rgb(102, 255, 102)',
                    'rgb(102, 255, 178)',
                    'rgb(102, 255, 255)',
                    'rgb(102, 178, 255)',
                    'rgb(102, 102, 255)',
                    'rgb(178, 102, 255)',
                    'rgb(255, 102, 255)',
                ],
                borderWidth: 1
            }]
        };
        const bar_config = {
            type: 'bar',
            data: bar_data,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        }

        return new Chart(this.c, bar_config)
    }
    
}

window.onload = ()=>{
    fetchData('jobposts').then(data => {
        new App(data)
    });
}
