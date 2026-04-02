// ==========================
// HTMX + Alpine.js 連携
// HTMXがコンテンツを差し替えた後、Alpine.jsコンポーネントを再初期化する
// ==========================
document.addEventListener('htmx:afterSwap', (event) => {
  if (typeof Alpine !== 'undefined') {
    Alpine.initTree(event.detail.target);
  }
});

// ==========================
// ロット管理ダイアログ（Alpine.jsコンポーネント）
// ==========================
function lotDialog() {
  return {
    dialogOpen: false,
    dialogMode: 'create',  // 'create' | 'edit'
    errorMsg: '',
    form: { lot_id: '', farm_name: '', house_name: '', plant_count: '' },

    // 新規登録ダイアログを開く
    openDialog() {
      this.dialogMode = 'create';
      this.errorMsg = '';
      this.form = { lot_id: '', farm_name: '', house_name: '', plant_count: '' };
      this.dialogOpen = true;
    },

    // 編集ダイアログを開く（DBからデータを取得してフォームに入力）
    async openEditDialog(lot_id) {
      this.errorMsg = '';
      const res = await fetch(`/lots/${lot_id}`);
      const lot = await res.json();
      this.form = {
        lot_id: lot.lot_id,
        farm_name: lot.farm_name,
        house_name: lot.house_name,
        plant_count: lot.plant_count,
      };
      this.dialogMode = 'edit';
      this.dialogOpen = true;
    },

    closeDialog() {
      this.dialogOpen = false;
    },

    // モードに応じてPOST / PATCHを切り替える
    async submitForm() {
      this.errorMsg = '';
      const isCreate = this.dialogMode === 'create';
      const url = isCreate ? '/lots' : `/lots/${this.form.lot_id}`;
      const method = isCreate ? 'POST' : 'PATCH';
      const { farm_name, house_name, plant_count } = this.form;
      const body = isCreate ? this.form : { farm_name, house_name, plant_count };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (res.ok) {
        // 成功後: コンテンツエリアをHTMXで再読み込み
        htmx.ajax('GET', '/lots', { target: '#content', swap: 'innerHTML' });
        this.closeDialog();
      } else {
        const err = await res.json();
        this.errorMsg = err.detail || (isCreate ? '登録に失敗しました' : '更新に失敗しました');
      }
    },
  };
}

// ==========================
// ユーザ管理ダイアログ（Alpine.jsコンポーネント）
// ==========================
function userDialog() {
  return {
    dialogOpen: false,
    dialogMode: 'create',  // 'create' | 'edit'
    errorMsg: '',
    form: { username: '', full_name: '', role: '' },

    // 新規登録ダイアログを開く
    openDialog() {
      this.dialogMode = 'create';
      this.errorMsg = '';
      this.form = { username: '', full_name: '', role: '' };
      this.dialogOpen = true;
    },

    // 編集ダイアログを開く（DBからデータを取得してフォームに入力）
    async openEditDialog(username) {
      this.errorMsg = '';
      const res = await fetch(`/users/${username}`);
      const user = await res.json();
      this.form = {
        username: user.username,
        full_name: user.full_name,
        role: user.role,
      };
      this.dialogMode = 'edit';
      this.dialogOpen = true;
    },

    closeDialog() {
      this.dialogOpen = false;
    },

    // モードに応じてPOST / PATCHを切り替える
    async submitForm() {
      this.errorMsg = '';
      const isCreate = this.dialogMode === 'create';
      const url = isCreate ? '/users' : `/users/${this.form.username}`;
      const method = isCreate ? 'POST' : 'PATCH';
      const { full_name, role } = this.form;
      const body = isCreate ? this.form : { full_name, role };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      if (res.ok) {
        // 成功後: コンテンツエリアをHTMXで再読み込み
        htmx.ajax('GET', '/users', { target: '#content', swap: 'innerHTML' });
        this.closeDialog();
      } else {
        const err = await res.json();
        this.errorMsg = err.detail || (isCreate ? '登録に失敗しました' : '更新に失敗しました');
      }
    },
  };
}
