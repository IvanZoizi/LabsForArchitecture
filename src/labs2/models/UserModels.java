package labs2.models;

import java.util.ArrayList;
import java.util.List;

public class UserModels<T> implements Models<T>{

    private final List<T> list = new ArrayList<>();

    @Override
    public List<T> get() {
        return new ArrayList<>(list);
    }

    @Override
    public boolean post(T data) {
        list.add(data);
        return true;
    }

    @Override
    public boolean update(T data, T newData) {

        int index = -1;
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).equals(data)) {
                index = i;
                break;
            }
        }

        if (index >= 0) {
            list.set(index, newData);
            return true;
        }

        return false;
    }

    @Override
    public boolean delete(T data) {

        int index = -1;
        for (int i = 0; i < list.size(); i++) {
            if (list.get(i).equals(data)) {
                index = i;
                break;
            }
        }

        if (index >= 0) {
            list.remove(index);
            return true;
        }

        return false;
    }
}
