var punchApp = new Vue({
      el: '#table',
      // jinja2のデリミタ {{}} と競合するため、デリミタを変更
      delimiters: ["[[", "]]"],
      data: {
        buttonStr: "修正",
        year: 2019,
        month: 1,
        items: [],
        // ユーザ側で編集する前の、サーバから取得した時点でのデータ
        hidenItems : []
      },
      mounted: function() {
        this.getRecords();
      },
      methods: {
        getRecords: function() {
          let axiosConfig = {
            headers: {
              'Content-Type': 'application/json;charset=UTF-8',
            }
          };
          axios.get('/attendance/get', {
              params: {
                year: 2019,
                month: 5
              }
            })
            .then(response => {
              let attendances = response.data;
              this.items = attendances;

            }).catch(error => {
              console.log(error);
            });
        },
        setNowYear: function() {
          this.year = 2019;
        },
        setNowMonth: function() {
          this.month = 5;
        },
        putRecords: function() {
          let axiosConfig = {
            headers: {
              'Content-Type': 'application/json;charset=UTF-8',
            }
          };
          // TODO: 送信の前に、形式が正しいかチェックする
          axios.post('/attendance/put',
            JSON.stringify({
                "records": this.items,
                "year": this.year,
                "month": this.month}),
                axiosConfig)
              .then(response => {
                let isSuccess = response.data;
                console.log(isSuccess);
                this.getRecords();
              }).catch(error => {
                console.log(error);
              });
            }
          }
        })
