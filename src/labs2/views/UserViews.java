package labs2.views;

import java.util.List;

public class UserViews<T> implements View<T> {

    @Override
    public void updateData(List<T> data) {
        System.out.println();
        for (T elem : data) {
            System.out.println(elem);
        }
        System.out.println();
    }
}
