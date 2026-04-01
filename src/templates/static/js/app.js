// ==========================
// ロット管理アプリ（Alpine.js）
// ==========================

function lotApp(initialLots) {
  return {
    lots: initialLots,
    dialogOpen: false,
    errorMsg: '',
    form: {
      lot_id: '',
      farm_name: '',
      house_name: '',
      plant_count: '',
    },

    // ダイアログを開く
    openDialog() {
      this.errorMsg = '';
      this.form = { lot_id: '', farm_name: '', house_name: '', plant_count: '' };
      this.dialogOpen = true;
    },

    // ダイアログを閉じる
    closeDialog() {
      this.dialogOpen = false;
    },

    // ロットを登録する
    async submitForm() {
      this.errorMsg = '';
      const res = await fetch('/api/lots', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.form),
      });

      if (res.ok) {
        const lot = await res.json();
        this.lots.unshift(lot); // 先頭に追加
        this.closeDialog();
      } else {
        const err = await res.json();
        this.errorMsg = err.detail || '登録に失敗しました';
      }
    },
  };
}
