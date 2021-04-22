# Tool gắn nhãn

## Requirements

### Dependencies

- Flask
- Pandas
- Numpy

Chạy dòng sau

```bash
!pip install flask pandas numpy
```

### Yêu cầu

- Trong folder `./static/files/` luôn phải có file `.csv` hợp lệ.
- Sau khi gắn toàn bộ nhãn, ấn submit để xuất kết quả ra file `test.csv`.
- Gắn xong có thể quay lại mà không mất những nhãn đã gắn.
- Trong trường hợp dữ liệu không cập nhật, ấn `Ctrl + Shift + R`.

## Sử dụng

Sau khi đã cài đặt các dependencies, đặc biệt là `Flask, Pandas, Numpy`, vào folder chứa file `app.py`, gõ vào lệnh sau:

```bash
python app.py
```

`Flask` sẽ mở một port trên hệ thống, thường là 5000. Upload file, gắn nhãn và  lưu file như bình thường.